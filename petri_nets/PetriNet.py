import numpy as np
import random
from graphviz import Digraph

class PetriNet:

    def __init__(self,
                 places,
                 transitions,
                 init_marking,
                 Aminus = np.array([]),
                 Aplus = np.array([]),
                 incidence_matrix = np.array([])):
        # Create some class instance variables
        self.incidence_matrix_ = np.array([])
        self.marking_ = np.array([])
        self.tokens_type_ = list()
        self.tokens_sequence_ = list()
        self.places_tokens = list(list())
        self.token_to_label_ = dict()
        self.label_to_token_ = dict()
        self.logic_transitions_ = list()
        self.transitions_logic_ = list()
        self.arcs_ = set()
        self.arcs_place_transition_ = set()
        self.arcs_transition_place_ = set()
        self.place_to_label_ = dict()
        self.label_to_place_ = dict()
        self.transition_to_label_ = dict()
        self.label_to_transition_ = dict()

        self.places_ = places.copy()
        for place_num in range(len(self.places_)):
            self.label_to_place_[places[place_num]] = place_num
            self.place_to_label_[place_num] = places[place_num]
        self.transitions_ = transitions.copy()
        for transition_num in range(len(self.transitions_)):
            self.label_to_transition_[transitions[transition_num]] = transition_num
            self.transition_to_label_[transition_num] = transitions[transition_num]
        self.init_marking_ = init_marking.copy()
        self.marking_ = init_marking.copy()
        self.Aminus_ = Aminus.copy()
        self.Aplus_ = Aplus.copy()
        if len(incidence_matrix != 0):
            self.incidence_matrix_ = incidence_matrix.copy()
        else:
            self.incidence_matrix_ = Aminus + Aplus

    def set_incidence_matrix(self, incidence_matrix):
        self.incidence_matrix_ = incidence_matrix

    def set_arcs_Aminus_Aplus(self):
        if len(self.Aminus_) !=0 and len(self.Aminus_) != 0:
            ## Add arcs from places to transitions
            num_rows_Aminus = np.shape(self.Aminus_)[0]
            num_cols_Aminus = np.shape(self.Aminus_)[1]
            for transition in range(num_rows_Aminus):
                for place in range(num_cols_Aminus):
                    # Add arc place, transition and weight if arc weight is nonzero
                    if self.Aminus_[transition, place] != 0:
                        arc = (place, transition, abs(self.Aminus_[transition, place]))
                        self.arcs_.add(arc)
                        self.arcs_place_transition_.add(arc)

            ## Add arcs from transitions to places
            num_rows_Aplus = np.shape(self.Aplus_)[0]
            num_cols_Aplus = np.shape(self.Aplus_)[1]
            for transition in range(num_rows_Aplus):
                for place in range(num_cols_Aplus):
                    # Add arc transition, place and weight if arc weight is nonzero
                    if self.Aplus_[transition,place] != 0:
                        arc = (transition, place, abs(self.Aplus_[transition, place]))
                        self.arcs_.add(arc)
                        self.arcs_transition_place_.add(arc)

        else:
            print("Arcs not being set because Aminus and Aplus are not set")

    def set_arcs_incidence_matrix(self):
        if len(self.incidence_matrix_ != 0):
            A = self.incidence_matrix_
            num_rows_A = np.shape(A)[0]
            num_cols_A = np.shape(A)[1]
            ## Iterate through incidence matrix
            for transition in range(num_rows_A):
                for place in range(num_cols_A):
                    # If number is negative, add an arc from place to transition
                    # That is, the transition consumes tokens from the place
                    if A[transition,place] < 0:
                        arc = (place, transition, abs(A[transition,place]))
                        self.arcs_.add(arc)
                        self.arcs_place_transition_.add(arc)
                    # If number is positive, add an arc from transition to place
                    # That is, the transition add tokens to the place
                    elif A[transition,place] > 0:
                        arc = (transition, place, abs(A[transition,place]))
                        self.arcs_.add(arc)
                        self.arcs_transition_place_.add(arc)
        else:
            print("Incidence matrix not set")

    def set_tokens_type(self,tokens_type):
        self.tokens_type_ = tokens_type.copy()
        for token_num in range(len(self.tokens_type_)):
            self.label_to_token_[self.tokens_type_[token_num]] = token_num
            self.token_to_label_[token_num] = self.tokens_type_[token_num]

    def set_places_tokens(self,places_tokens):
        self.places_tokens = places_tokens.copy()

    def set_logic_transitions(self, logic_transitions):
        self.logic_transitions_ = logic_transitions.copy()

    def set_tokens_sequence(self, tokens_sequence):
        self.tokens_sequence_ = tokens_sequence.copy()

    def set_transitions_logic(self, transitions_logic):
        self.transitions_logic_ = transitions_logic.copy()

    def print(self):
        print("Places:")
        print(self.places_)

        print("Transitions:")
        print(self.transitions_)

        print("Initial marking:")
        print(self.init_marking_)

        print("Aminus:")
        print(self.Aminus_)

        print("Aplus:")
        print(self.Aplus_)

        print("Arcs:")
        print(self.arcs_)

        print("Arcs (place,transition):")
        print(self.arcs_place_transition_)

        print("Arcs (transition, place):")
        print(self.arcs_transition_place_)

        print("Incidence matrix:")
        print(self.incidence_matrix_)

    def plot(self, filename, show_output):

        ## Create graph
        net = Digraph(comment=filename)

        ## Print horizontally
        net.attr(rankdir='LR', size='8.5')

        ## Create net places
        for place in self.places_:
            place_label = place
            if self.marking_[self.label_to_place_[place]] != 0:
                place_marking = str(self.marking_[self.label_to_place_[place]])
            else:
                place_marking = ""
            net.attr('node', shape='circle', fontsize='12')
            net.node(place, label=place_marking, xlabel=place_label)

        ## Create net transitions
        for transition in self.transitions_:
            transition_label = transition
            net.attr('node', shape='square', fontsize='12')
            net.node(transition, label="", xlabel=transition_label)

        ## Create place->transition edges
        for edge in self.arcs_place_transition_:
            node1 = str(self.place_to_label_[edge[0]])
            node2 = str(self.transition_to_label_[edge[1]])
            edge_weight = str(edge[2])
            # If edge weight equals 1, do not plot 1 to make drawing clearer
            if edge[2] == 1:
                net.edge(node1, node2)
            else:
                net.edge(node1, node2, edge_weight)

        ## Create transition->place edges
        for edge in self.arcs_transition_place_:
            node1 = str(self.transition_to_label_[edge[0]])
            node2 = str(self.place_to_label_[edge[1]])
            edge_weight = str(edge[2])
            # If edge weight equals 1, do not plot 1 to make drawing clearer
            if edge[2] == 1:
                net.edge(node1, node2)
            else:
                net.edge(node1, node2, edge_weight, fontsize='12')

        ## Create net pdf and open it
        net.render(filename, view=show_output)

    def next_marking(self, u):
        print("Input u:")
        print(u)
        # If incidence matrix is initialized
        if len(self.incidence_matrix_) == len(u):
            # Fire transition and get new marking
            marking = self.marking_ + np.matmul(u,self.incidence_matrix_)
        else:
            print("Incidence matrix not initialized. Returning initial marking:")
            marking = self.init_marking_
        self.marking_ = marking
        print("Next marking:")
        print(self.marking_)
        return marking

    def enabled_transitions(self):
        enabled_transitions = set()
        for transition in self.transitions_:
            ## Assume transition starts enabled
            transition_enabled = True
            ## Get corresponding input edges to transition
            for arc in self.arcs_place_transition_:
                arc_place = arc[0]
                arc_transition = arc[1]
                arc_weight = arc[2]
                ## If arc transition corresponds to the transition
                if arc_transition == self.label_to_transition_[transition]:
                    ## Check for all places that have edges input to the transition
                    # if the place marking is lower than the arc_weight
                    for place in range(len(self.marking_)):
                        if place == arc_place:
                            if self.marking_[place] < arc_weight:
                                transition_enabled = False

            if transition_enabled == True:
                enabled_transitions.add(transition)

        return enabled_transitions

    def run_net(self):
        transition_to_fire = ''
        transitions_firing_num = np.zeros(len(self.transitions_))
        while True:
            print("-----------------------------------")
            if transition_to_fire == "exit":
                break
            print("Transitions labels:")
            print(self.transitions_)
            print("Enabled transitions:")
            print(self.enabled_transitions())
            print("Enter transition to fire:")
            transition_to_fire = input()
            # If transition label is wrong, ask for new transition label
            if transition_to_fire not in self.transitions_ or transition_to_fire not in self.enabled_transitions():
                print("Wrong transition label or transition not enabled!")
            else:
                print("Transition number:")
                transition_number = self.label_to_transition_[transition_to_fire]
                print(transition_number)

                # Apply transitions logic if any
                if transition_to_fire in self.logic_transitions_:
                    # Get logic of transition as a lambda function
                    transition_condition = self.transitions_logic_[transition_number](transitions_firing_num[transition_number])
                    print(transition_condition)

                    # Update number of firings
                    transitions_firing_num[transition_number] += 1

                # Initialize input vector with zeros
                u = np.zeros(len(self.transitions_))
                # Make respective transition equals 1 to fire it
                u[transition_number] = 1
                print("Input vector:")
                print(u)

                # Run net after firing transition
                self.next_marking(u)

                self.plot("net_state",True)

    def transition_logic(self,
                         transition_to_fire,
                         transition_number,
                         transitions_firing_num):
        if transition_number == 0:
            transition_condition = self.transitions_logic_[transition_number](transitions_firing_num[transition_number])
        if transition_number == 1:
            transition_condition = self.transitions_logic_[transition_number](transitions_firing_num[transition_number])


    def run_net_randomly(self, num_steps):
        transitions_fired = list()
        markings = list()
        markings.append(self.marking_)
        for step in range(num_steps):
            print("-----------------------------------")
            # Get enabled transitions
            enabled_transitions = self.enabled_transitions()
            # Select randomly transition to fire
            transition_to_fire = random.sample(enabled_transitions,1)[0]
            print("Transition to fire:")
            print(transition_to_fire)
            transitions_fired.append(transition_to_fire)
            transition_number = self.label_to_transition_[transition_to_fire]
            # Initialize input vector with zeros
            u = np.zeros(len(self.transitions_))
            # Make respective transition equals 1 to fire it
            u[transition_number] = 1
            # Ru net after firing transition
            self.next_marking(u)
            markings.append(self.marking_)

        return transitions_fired, markings

    def control_net(self, net_constraints_matrix, net_constraints_vector):
        controller_incidence_matrix = -np.matmul(self.incidence_matrix_,net_constraints_matrix)
        print("Controller incidence matrix:")
        print(controller_incidence_matrix)

        controller_init_marking = net_constraints_vector - np.matmul(self.init_marking_,net_constraints_matrix)
        print("Controller initial marking:")
        print(controller_init_marking)

        complete_incidence_matrix = np.concatenate((self.incidence_matrix_, controller_incidence_matrix), axis=1)
        print("Complete incidence matrix:")
        print(complete_incidence_matrix)

        complete_init_marking = np.concatenate((self.init_marking_, controller_init_marking))
        print("Complete initial marking:")
        print(complete_init_marking)

        # Update incidence matrix
        self.incidence_matrix_ = complete_incidence_matrix

        # Update init marking and marking
        self.init_marking_ = complete_init_marking
        self.marking_ = complete_init_marking

        # Add control places to net places
        for control_place in range(len(controller_init_marking)):
            self.places_.append("C"+str(control_place))

        # Clear dictionaries
        self.label_to_place_ = dict()
        self.place_to_label_ = dict()

        # Update dictionaries
        for place_num in range(len(self.places_)):
            self.label_to_place_[self.places_[place_num]] = place_num
            self.place_to_label_[place_num] = self.places_[place_num]







