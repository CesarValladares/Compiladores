
states = []
last_state = 0
automata = []

def createNFA(regex, star): 

    global last_state
    parent = False
    p_counter = 0
    mini_regex = ''
    state_before = last_state

    print("AN", regex, star)

    for index, char in enumerate(regex):

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

                    createNFA(mini_regex, True)

                else: 
                    createNFA(mini_regex, False)

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

                print("STAAR")
                state = [Num_f_state, 'ep', or_las_state]
                automata.append(state)

                star = False

            last_state = Num_f_state

        else: 

            state = [last_state, char, last_state +1]
            last_state += 1
            automata.append(state)

    if star:
        print ("STAR 2")
        state = [last_state, 'ep', state_before]



# regex = input("Enter Regex\n")
regex = "((z)(a|bc|de)*)*"
print("REGEX", regex)
createNFA(regex, False)
for states in automata:
    print(states)