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
                ## Print event and next state for that event
                print(event, "->", transition[1][event])

        print("Initial state")
        print(self.initial_state_)

        print("Marked states")
        for state in self.marked_states_:
            print(state)

        print("Event alphabet")
        for event in self.alphabet_:
            print(event)