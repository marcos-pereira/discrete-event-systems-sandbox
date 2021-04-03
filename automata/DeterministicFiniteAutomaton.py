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
        for state in sorted(self.states_):
            print(state)

        print("Transitions")
        for transition in self.transitions_.items():
            ## Print transition state
            print("State ", transition[0])

            for event in self.alphabet_:
                ## Check if the transition exists
                if transition[1] and event in transition[1]:
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

    def plot_automaton(self, filename, show_output):

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
            ## Check if state is still a state of the automaton
            ## A state may have been removed due to some automata operation
            if transition[0] in self.states_:
                for event in self.alphabet_:
                    ## Check if transition exists
                    if transition[1] and event in transition[1]:
                        node1 = transition[0]
                        node2 = transition[1][event]
                        automaton.edge(node1,node2, label=event)

        ## Create automaton pdf and open it
        automaton.render(filename, view=show_output)

    def reachable_automaton(self):

        ## Reference: http://www.cs.um.edu.mt/gordon.pace/Research/Software/Relic/Transformations/FSA/remove-unreachable.html

        ## Initially, only the initial state is reachable
        reachable_states = {self.initial_state_}
        print(reachable_states)

        ## The initial state is added
        element_added = True

        ## While an elment is added to the set
        while element_added:
            [reachable_states, element_added] = self.reachable_states(reachable_states)

        print("Reachable states:")
        print(reachable_states)

        ## Update automaton states
        self.states_ = reachable_states.copy()

        ## Initially, all transitions are valid
        reachable_transitions = self.transitions_.copy()

        ## Remove unecessary transitions
        for transition in self.transitions_.items():
            if transition[0] not in self.states_:
                del reachable_transitions[transition[0]]

        ## Update automaton transitions
        self.transitions_ = reachable_transitions.copy()


    def reachable_states(self, states):

        reachable_states = states.copy()
        init_states = states.copy()

        for state in states:
            ## Get transitions of the state
            transition = self.transitions_[state]

            ## Check all transitions of the state
            for event in transition:
                ## Check if the transition leads to a new state
                if transition[event] != state:
                    reachable_states.add(transition[event])

        ## If the size of the set changes, at least an element has been added
        if len(reachable_states) != len(init_states):
            element_added = True
        else:
            element_added = False

        return reachable_states, element_added

    def coaccessible_automaton(self):

        ## The initial state is added
        element_added = True

        ## While an elment is added to the set
        # while element_added:
        #     [coaccessible_states, element_added] = self.coaccessible_states(coaccessible_states)

        # [coaccessible_states, element_added] = self.coaccessible_states(self.states_)

        coaccessible_states = set()
        for state in self.states_:
            print("--------")
            print(state)
            if self.coaccessible_states2(state):
                coaccessible_states.add(state)

        print("Coaccessible states:")
        print(coaccessible_states)

        ## Update automaton states
        self.states_ = coaccessible_states.copy()

        ## Initially all transitions are valid
        reachable_transitions = self.transitions_.copy()

        ## Remove unecessary transitions
        # for state in self.states_:
        #     ## Get transitions of the state
        #     transitions = self.transitions_[state]
        #
        #     ## Remove transitions that lead to removed states
        #     for transition in transitions:
        #         for event in self.alphabet_:
        #             if transition[1][event] not in self.states_:
        #                 del reachable_transitions[transition]

        ## Remove unecessary transitions
        for transition in self.transitions_.items():
            ## Check if state is still a state of the automaton
            ## A state may have been removed due to some automata operation
            if transition[0] in self.states_:
                for event in self.alphabet_:
                    ## Check if transition next state does not exist, remove it
                    if transition[1][event] not in self.states_:
                        del reachable_transitions[transition[0]][event]


        ## Update automaton transitions
        self.transitions_ = reachable_transitions.copy()

    def coaccessible_states(self, states):

        coaccessible_states = set()
        init_states = states.copy()

        for state in states:
            ## Get transitions of the state
            transition = self.transitions_[state]

            ## Check all transitions of the state
            for event in transition:
                ## Check if the transition leads to a marked state or if the state is marked
                if transition[event] in self.marked_states_ or state in self.marked_states_:
                    coaccessible_states

        ## If the size of the set changes, at least an element has been added
        if len(coaccessible_states) != len(init_states):
            element_added = True
        else:
            element_added = False

        return coaccessible_states, element_added

    def coaccessible_states2(self, state):

        ## Get transitions of the state
        transition = self.transitions_[state]
        print("state "+state)
        print(transition)

        ## Check all transitions of the state
        for event in transition:
            print(transition[event])
            ## Check if the transition leads to a marked state or if the state is marked
            if transition[event] in self.marked_states_ or state in self.marked_states_:
                return True
            elif transition[event]:
                return False
            else:
                self.coaccessible_states2(transition[event])










