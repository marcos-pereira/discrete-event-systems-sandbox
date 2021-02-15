import numpy as np
from graphviz import Digraph

class PetriNet:

    incidence_matrix_ = np.array([])
    marking_ = np.array([])
    arcs_ = set()
    arcs_place_transition_ = set()
    arcs_transition_place_ = set()
    place_to_label_ = dict()
    label_to_place_ = dict()
    transition_to_label_ = dict()
    label_to_transition_ = dict()

    def __init__(self,
                 places,
                 transitions,
                 init_marking,
                 Aminus = np.array([]),
                 Aplus = np.array([]),
                 incidence_matrix = np.array([])):
        self.places_ = places
        for place_num in range(len(self.places_)):
            self.label_to_place_[places[place_num]] = place_num
            self.place_to_label_[place_num] = places[place_num]
        self.transitions_ = transitions
        for transition_num in range(len(self.transitions_)):
            self.label_to_transition_[transitions[transition_num]] = transition_num
            self.transition_to_label_[transition_num] = transitions[transition_num]
        self.init_marking_ = init_marking
        self.marking_ = init_marking
        self.Aminus_ = Aminus
        self.Aplus_ = Aplus
        if len(incidence_matrix != 0):
            self.incidence_matrix_ = incidence_matrix
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
        print("Transitions to fire:")
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

                # Initialize input vector with zeros
                u = np.zeros(len(self.transitions_))
                # Make respective transition equals 1 to fire it
                u[transition_number] = 1
                print("Input vector:")
                print(u)

                # Run net after firing transition
                self.next_marking(u)

                self.plot("net_state",True)





