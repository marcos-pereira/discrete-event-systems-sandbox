from graphviz import Digraph

class DeterministicFiniteAutomaton:

    def __init__(self, states, transitions, initial_state, marked_states, alphabet):
        print("Initializing automaton...")
        self.states_ = states.copy()
        self.transitions_ = transitions.copy()
        self.initial_state_ = initial_state
        self.marked_states_ = marked_states.copy()
        self.alphabet_ = alphabet.copy()

    def print_automaton(self):
        print("States")
        for state in self.states_:
            print(state)

        print("Transitions")
        for transition in self.transitions_.items():
            ## Print transition state
            print("State ", transition[0])

            for event in self.alphabet_:
                ## Check if the transition exists
                if transition[1]:
                    ## Print event and next state for that event
                    print(event, "->", transition[1][event])
                else:
                    print(event, "--")

        print("Initial state")
        print(self.initial_state_)

        print("Marked states")
        for state in self.marked_states_:
            print(state)

        print("Event alphabet")
        for event in self.alphabet_:
            print(event)
            
    def run(self, event_sequence):
        print("Running automaton for the event sequence " + event_sequence)

        current_state = self.initial_state_
        print("Initial state " + current_state)

        for event in event_sequence:
            if(self.transitions_[current_state]):
                current_state = self.transitions_[current_state][event]
                print("State " + current_state)

        if current_state in self.marked_states_:
            print("Reached marked state")
        else:
            print("Event sequence not accepted")

    def plot_automaton(self, filename):

        ## Create graph
        automaton = Digraph(comment=filename)

        ## Print horizontally
        automaton.attr(rankdir='LR', size='8.5')

        ## Create automaton states
        for state in self.states_:


            ## Check if it is initial state
            if state == self.initial_state_:
                state_label = 'INIT:'+ state
            else:
                state_label = state

            ## If state is marked, draw doublecircle
            if state in self.marked_states_:
                automaton.attr('node', shape='doublecircle')
            else:
                automaton.attr('node', shape='circle')

            automaton.node(state, state_label)

        ## Create transitions
        for transition in self.transitions_.items():
            for event in self.alphabet_:
                ## Check if transition exists
                if transition[1]:
                    node1 = transition[0]
                    node2 = transition[1][event]
                    automaton.edge(node1,node2, label=event)

        ## Create automaton pdf and open it
        automaton.render(filename, view=True)








