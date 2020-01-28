import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

states = [0]
last_state = 0
counter_state = 0
automata = []
alphabet = []
special = ['(', ')', '|']

def createNFA(regex, star, finish): 

    print("REGES", regex, star)

    global last_state
    global counter_state
    parent = False
    p_counter = 0
    mini_regex = ''
    state_before = last_state

    if star == True:

        state = [last_state, 'ep', last_state+1+counter_state]
        last_state += (1 + counter_state)
        if counter_state != 0: counter_state = 0

        if state not in automata:
            automata.append(state)

    for index, char in enumerate(regex):

        if char not in alphabet and char not in special:
            alphabet.append(char)

        if char == '(':
            parent = True            
            if p_counter > 0:
                mini_regex+= char

            p_counter += 1

        elif char == ')':

            p_counter -= 1

            if p_counter > 0:
                mini_regex+= char

            elif p_counter == 0:
                if index < len(regex) -1 and regex[index +1] == '*':

                    createNFA(mini_regex, True, 0)


                else: 
                    createNFA(mini_regex, False, 0)

                mini_regex = ''

        elif p_counter > 0:
                mini_regex+= char
       
    if parent == False:
        if '|' in regex:
            or_states = regex.split('|')
            f_states = regex.replace('|', '')
            Num_f_state = last_state + len(f_states) +1

            or_las_state = last_state

            for or_state in or_states:

                for index, char in enumerate(or_state):
                    
                    if index == 0:
                        state = [or_las_state, char, last_state + 1 +counter_state]
                    else:
                        state = [last_state, char, last_state + 1 +counter_state]

                    last_state += (1 + counter_state)
                    if counter_state != 0: counter_state = 0

                    if state not in automata:
                        automata.append(state)

                    if last_state not in states:
                        states.append(last_state)

                    if index == len(or_state) -1:       
                        state = [last_state, 'ep', Num_f_state]
                        if state not in automata:
                            automata.append(state)

            if star == True: 

                state = [Num_f_state, 'ep', or_las_state]
                if state not in automata:
                    automata.append(state)

                star = False

            last_state = or_las_state            

            if last_state not in states:
                states.append(last_state)

        else: 

            star_states = 1

            for char in regex:
                state = [last_state, char, last_state +1]
                last_state += 1
                star_states += 1

                if state not in automata:
                    automata.append(state)

            if star == True:
                state = [last_state, 'ep', state_before]
                if state not in automata:
                    automata.append(state)

                counter_state = star_states
                last_state = state_before

    if star:
        state = [last_state, 'ep', state_before]
        last_state = state_before

def epsilon_closure(states):
    
    for state in states:
        for nfa_state in automata:
            if nfa_state[0] == state and nfa_state[1] == 'ep' and not nfa_state[2] in states:
                 states.append(nfa_state[2])
    
    return states

def move(state,symbol):
    temp = []
    for s in state:
        for nfa_state in automata:
            if nfa_state[0] == s and nfa_state[1] == symbol and not nfa_state[2] in temp:
                temp.append(nfa_state[2])

    temp = epsilon_closure(temp)

    return temp

def isNew(state,new_states):

    for n in new_states:
        if set(n) == set(state):
            return 0

    return 1

def NFA_to_DFA(nfa_initial_state,nfa_final_state,alphabet):

    dfa = {}
    DFA = []
    current_state = []
    final_states = []
    new_states = []


    initial_state = [nfa_initial_state]

    current_state = epsilon_closure(initial_state)
    
    new_states.append(current_state)

    if nfa_final_state in current_state:
        final_states.append(current_state)

    for state in new_states:
        for symbol in alphabet:

            current_state = move(state,symbol)

            if current_state:

                if isNew(current_state,new_states):
                    new_states.append(current_state)
                    if nfa_final_state in current_state:
                        final_states.append(current_state)

                DFA.append([new_states.index(state),symbol,new_states.index(current_state)])

    dfa["dfa"] = DFA
    dfa["states"] = new_states
    dfa["final_states"] = final_states

    return dfa
    
def EvaluateString(cadena, ODFA):
    dfa = ODFA["dfa"]
    ini = 0
    valid = False

    for char in cadena:

        found = False

        for index, state in enumerate(dfa):
            if state[0] == ini:
                if state[1] == char:
                    found = True
                    ini = state[2]
                    break

                
        if found == False:            
            ini = -1

                
    for final in ODFA["final_states"]:
        if ini == ODFA["states"].index(final):
            valid = True
    
    return valid


regex = input("Enter Regex\n")
createNFA(regex, False, 1)

dfa = NFA_to_DFA(0, last_state, alphabet)

# Grafico
g = nx.DiGraph()
g2 = nx.DiGraph()
g.add_nodes_from(states)

# Datos de NFA
print("NFA")
for state in automata:
    print(state)

    g.add_edge(state[0], state[2])


# Datos de DFA
print("DFA")
for a in dfa["dfa"]:
    g2.add_edge(a[0], a[2])
    print(a)

print("DFA final states:")
for final in dfa["final_states"]:
    print(dfa["states"].index(final))


nx.draw(g,with_labels=True, arrows=True)
plt.draw()
plt.show()

nx.draw(g2,with_labels=True, arrows=True)
plt.draw()
plt.show()

while True:
    cadena = input("Enter string\n")
    print(EvaluateString(cadena, dfa))
