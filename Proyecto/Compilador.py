import ply.lex as lex
import ply.yacc as yacc
import os
import sys
sys.path.insert(0, "../..")


class Parser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        self.arrays = {}
        self.lines_loop = []
        self.counter_lines = []
        self.current_line = ''
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        # print self.debugfile, self.tabmodule

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        while 1:
            try:
                s = input('lobo > ')
            except EOFError:
                break
            if not s:
                continue

            yacc.parse(s)

    def readFile(self, fileName):

        file1 = open(fileName, 'r')
        lines = file1.readlines()

        for i, line in enumerate(lines):

            try:
                self.current_line = line
                
                if 'for' in line:
                
                    line = line.replace('for', '')
                    line = line.replace('(', '')
                    line = line.replace(')', '')
                    line = line.replace(' ', '')
                    line = line.replace('{', '')
                    line = line.replace('\n', '')

                    args = line.split(';')

                    aux_line = ''
                    aux_i = i              

                    while '}' not in aux_line:

                        if '}' in aux_line:
                            break

                        aux_i += 1
                        aux_line = lines[aux_i].replace("\n",'')
                        
                        if '}' not in aux_line:
                            self.lines_loop.append(aux_line)
                            self.counter_lines.append(aux_i)

                    start_for = self.names[args[0]]    
                    
                    for algo in range(start_for, int(args[1]), int(args[2])):

                        if self.names[args[0]] + int(args[2]) < int(args[1]):
                                                    
                            self.names[args[0]] += int(args[2])
                            for loop_line in self.lines_loop:
                                yacc.parse(loop_line)

                else:
                    

                    if i not in self.counter_lines and '}' not in line:
                        self.lines_loop = []
                        self.counter_lines = []
                        yacc.parse(line)

            except EOFError:

                print("Error in line ", i, line)


class Calc(Parser):

    reserved = {
        'print' : 'PRINT',
        'for' : 'FOR',
        'if' : 'IF',
        'then' : 'THEN',
        'else' : 'ELSE',
        'while' : 'WHILE'
    }

    tokens = [
        'NUMBER',
        'ID',
        'FLOAT',
        'STRING',
        'CHAR',
        'EXP',
        'PLUS',
        'MINUS',
        'TIMES',
        'EQUALS',
        'DIVIDE',
        'FACTORIAL',
        'SQUARE',
        'LPAREN',
        'RPAREN',
        'LKEY',
        'RKEY',
        'COMMA',
        'COMMENT',
        'FORFUNC',
        'LBRACKET',
        'RBRACKET',
        'LESSTHAN',
        'LESSOREQUAL',
        'MORETHAN',
        'MOREOREQUAL',
        'SAME',
        'SEMICOLON',
        
    ] + list(reserved.values())
    
    t_LESSTHAN = r'<'
    t_MORETHAN = r'>'
    t_MOREOREQUAL = r'>='
    t_LESSOREQUAL = r'<='
    t_SAME = r'=='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_FACTORIAL = r'!'
    t_SQUARE = r'¬'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LKEY = r'\{'
    t_RKEY = r'\}'
    t_EQUALS = r'='
    t_EXP = r'\*\*'
    t_STRING = r'\'[a-zA-Z_][a-zA-Z0-9_ ]*\''
    t_COMMA = r','
    t_SEMICOLON = r'\;'

    def t_ID(self, p):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        p.type = self.reserved.get(p.value,'ID')
        return p

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        # print "parsed number %s" % repr(t.value)
        return t

    def t_COMMENT(self, t):
        r'\#.*'
        pass
        # No return value. Token discarded

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('left', 'PLUS', 'MINUS', 'MORETHAN', 'LESSTHAN', 'MOREOREQUAL', 'LESSOREQUAL', 'SAME'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EXP', 'LPAREN'),
        ('right', 'UMINUS'),
    )

    def p_statement_assign(self, p):
        '''statement : ID EQUALS expression'''

        if len(p) == 4:
            self.names[p[1]] = p[3]

    def p_statement_print(self, p):
        '''statement : PRINT expression'''

        print(p[2])
        

    def p_statement_list(self, p):
        '''statement : ID EQUALS LBRACKET statement RBRACKET
                    | statement COMMA NUMBER
                    | NUMBER '''

        if len(p) == 2:
            p[0] = [p[1]]

        elif len(p) == 4:
            p[0] = p[1] + [p[3]]

        else:
            self.arrays[p[1]] = p[4]


    def p_statement_expr(self, p):
        'statement : expression'
        print(p[1])


    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXP expression
        """

        if isinstance(p[1], int) == False or isinstance(p[3], int) == False:

            print("Syntax error")

        else:

            if p[2] == '+':
                p[0] = p[1] + p[3]
            elif p[2] == '-':
                p[0] = p[1] - p[3]
            elif p[2] == '*':
                p[0] = p[1] * p[3]
            elif p[2] == '/':
                p[0] = p[1] / p[3]
            elif p[2] == '**':
                p[0] = p[1] ** p[3]

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

    def p_expression_data_in_array(self, p):
        'expression : ID LBRACKET NUMBER RBRACKET'

        try:
            array = self.arrays[p[1]]

            try:
                p[0] = array[p[3]]

            except LookupError:    
                print ("index out of range in", self.current_line)

        except LookupError:
            print("Undefined string '%s'" % p[1])
            p[0] = 0

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_expression_string(self, p):
        'expression : STRING'
        p[0] = p[1]

    def p_expression_ID(self, p):
        'expression : ID'
        try:
            p[0] = self.names[p[1]]

        except:
            try:
                p[0] = self.arrays[p[1]]

            except LookupError:
                print("Undefined string '%s'" % p[1])
                p[0] = 0

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value, p)
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':

    calc = Calc()


    try: 
        fileName = sys.argv[1]

        if fileName.endswith('.lb'):
            calc.readFile(fileName)
        else:
            print("Extension error")
    except:
        
        calc.run()
