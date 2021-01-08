#!/usr/bin/env python

from DeterministicFiniteAutomaton import DeterministicFiniteAutomaton

def main():
    print("main()...")

    states = ['0','1']
    transitions = {
        '0':{'a':'1','b':'0'},
        '1':{'a':'1','b':'0'}
    }
    initial_state = '0'
    marked_states = ['1']
    alphabet = ['a','b']
    event_sequence = 'aaba'

    dfa = DeterministicFiniteAutomaton(states, transitions, initial_state, marked_states, alphabet)

    dfa.print_automaton()
    dfa.run(event_sequence)

if __name__ == '__main__':

    main()