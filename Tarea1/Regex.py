import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

states = []
last_state = 0
automata = []
alphabet = []
special = ['(', ')', '|']

def createNFA(regex, star, finish): 
    global last_state
    parent = False
    p_counter = 0
    mini_regex = ''
    state_before = last_state

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
                        state = [or_las_state, char, last_state + 1]
                    else:
                        state = [last_state, char, last_state + 1]

                    last_state += 1                    
                    automata.append(state)

                    if index == len(or_state) -1:       
                        state = [last_state, 'ep', Num_f_state]
                        automata.append(state)

            if star == True: 
                state = [Num_f_state, 'ep', or_las_state]
                automata.append(state)

                star = False

            last_state = Num_f_state

        else: 

            for char in regex:
                state = [last_state, char, last_state +1]
                last_state += 1
                automata.append(state)

            if star == True:

                state = [last_state, 'ep', state_before]
                automata.append(state)

            

    if star:
        state = [last_state, 'ep', state_before]

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
    

# regex = input("Enter Regex\n")
regex = "(ab|cd)"
print("REGEX", regex)
createNFA(regex, False, 1)

dfa = NFA_to_DFA(0, last_state, alphabet)

print("NFA")
for states in automata:
    print(states)

print("DFA")
for a in dfa["dfa"]:
    print(a)

print("DFA final states:")
for final in dfa["final_states"]:
    print(dfa["states"].index(final))


g = nx.DiGraph()
g.add_nodes_from([1,2,3,4,5])
g.add_edge(1,2)
g.add_edge(4,2)
g.add_edge(3,5)
g.add_edge(2,3)
g.add_edge(5,4)

nx.draw(g,with_labels=True)
plt.draw()
plt.show()
pylab.show()
