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
        self.arrays = []
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
                yacc.parse(line)
            except EOFError:

                print("Error in line ", i, line)


class Calc(Parser):

    tokens = (
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
        'LLLAVE',
        'RLLAVE',
        'COMMA',
        'COMMENT',
        'array'
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_FACTORIAL = r'!'
    t_SQUARE = r'¬'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LLLAVE = r'\['
    t_RLLAVE = r'\]'
    t_EQUALS = r'='
    t_EXP = r'\*\*'
    t_STRING = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_COMMA = r','

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
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EXP'),
        ('right', 'UMINUS'),
    )

    def p_statement_assign(self, p):
        'statement : STRING EQUALS expression'
        self.names[p[1]] = p[3]

    def p_statement_list(self, p):
        '''statement : STRING EQUALS LLLAVE statement RLLAVE
                    | statement COMMA NUMBER
                    | NUMBER '''

        if len(p) == 2:
            p[0] = [p[1]]

        elif len(p) == 4:
            p[0] = p[1] + [p[3]]

        else:
            p[0] = p[4]
            array = [p[1], p[0]]
            self.arrays.append(array)

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

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_expression_string(self, p):
        'expression : STRING'
        try:
            p[0] = self.names[p[1]]

        except:
            try:
                for array in self.arrays:
                    if array[0] == p[1]:
                        p[0] = array[1]

            except LookupError:
                print("Undefined string '%s'" % p[1])
                p[0] = 0

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
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
