#!/usr/bin/env python

from DeterministicFiniteAutomaton import DeterministicFiniteAutomaton

def main():
    print("main()...")

    states = {'0','1','2','3','4'}
    transitions = {
        '0':{'a':'1','b':'0'},
        '1':{'a':'2','b':'0'},
        '2':{'b':'3'},
        '3':{'a':'2','b':'1'},
        '4':{'b':'3'}
    }
    initial_state = '0'
    marked_states = {'1'}
    alphabet = {'a','b'}
    event_sequence = 'aaba'

    dfa = DeterministicFiniteAutomaton(states, transitions, initial_state, marked_states, alphabet)

    ## Show automaton plot output
    show_output = True

    ## Print automaton
    dfa.print_automaton()
    dfa.run(event_sequence)
    dfa.plot_automaton('automaton1', show_output)

    ## Convert automaton to get accessible part
    # dfa.reachable_automaton()
    # dfa.print_automaton()
    # dfa.plot_automaton('reachable_automaton', show_output)

    ## Convert automaton to get accessible part
    # dfa.coaccessible_automaton()
    # dfa.print_automaton()
    # dfa.plot_automaton('coaccessible_automaton', show_output)

    # Light bulb automaton
    states = {'on', 'off'}
    transitions = {
        'on': {'turn_off': 'off'},
        'off': {'turn_on': 'on'},
    }
    initial_state = 'off'
    marked_states = {'on'}
    alphabet = {'turn_on', 'turn_off'}
    event_sequence = 'turn_on'+'turn_off'

    dfa = DeterministicFiniteAutomaton(states, transitions, initial_state, marked_states, alphabet)

    ## Show automaton plot output
    show_output = True

    ## Print automaton
    dfa.print_automaton()
    # dfa.run(event_sequence)
    dfa.plot_automaton('light_bulb', show_output)

    ## Client queue
    states = {'empty_queue', 'one_client', 'two_clients'}
    transitions = {
        'empty_queue': {'arrive': 'one_client'},
        'one_client': {'arrive': 'two_clients','enter_server':'empty_queue'},
        'two_clients': {'enter_server':'one_client'}
    }
    initial_state = 'empty_queue'
    marked_states = {'empty_queue'}
    alphabet = {'arrive', 'enter_server'}

    dfa = DeterministicFiniteAutomaton(states, transitions, initial_state, marked_states, alphabet)

    ## Show automaton plot output
    show_output = True

    ## Print automaton
    dfa.print_automaton()
    # dfa.run(event_sequence)
    dfa.plot_automaton('queue', show_output)

    ## Client server
    states = {'empty_server', 'serving_client'}
    transitions = {
        'empty_server': {'enter_server': 'serving_client'},
        'serving_client': {'leave_server': 'empty_server'},
    }
    initial_state = 'empty_server'
    marked_states = {'empty_server'}
    alphabet = {'enter_server', 'leave_server'}

    dfa = DeterministicFiniteAutomaton(states, transitions, initial_state, marked_states, alphabet)

    ## Show automaton plot output
    show_output = True

    ## Print automaton
    dfa.print_automaton()
    # dfa.run(event_sequence)
    dfa.plot_automaton('server', show_output)

if __name__ == '__main__':

    main()