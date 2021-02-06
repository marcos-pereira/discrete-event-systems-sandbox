import numpy as np
from graphviz import Digraph

class PetriNet:

    incidence_matrix_ = np.array([])
    arcs_ = set()
    arcs_place_transition_ = set()
    arcs_transition_place_ = set()
    place_to_label_ = dict()
    label_to_place_ = dict()
    transition_to_label_ = dict()

    def __init__(self, places, transitions, init_marking, Aminus = np.array([]), Aplus = np.array([])):
        self.places_ = places
        for place_num in range(len(self.places_)):
            self.label_to_place_[places[place_num]] = place_num
            self.place_to_label_[place_num] = places[place_num]
        self.transitions_ = transitions
        for transition_num in range(len(self.transitions_)):
            self.transition_to_label_[transition_num] = transitions[transition_num]
        self.init_marking_ = init_marking
        self.Aminus_ = Aminus
        self.Aplus_ = Aplus
        self.incidence_matrix_ = Aminus + Aplus

    def set_incidence_matrix(self, incidence_matrix):
        self.incidence_matrix_ = incidence_matrix

    def set_arcs(self):
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
                    # Add arc place, transition and weight if arc weight is nonzero
                    if self.Aplus_[transition,place] != 0:
                        arc = (transition, place, abs(self.Aplus_[transition, place]))
                        self.arcs_.add(arc)
                        self.arcs_transition_place_.add(arc)

        else:
            print("Arcs not being set because Aminus and Aplus are not set")

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
            if self.init_marking_[self.label_to_place_[place]] != 0:
                place_marking = str(self.init_marking_[self.label_to_place_[place]])
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
            net.edge(node1, node2, edge_weight)

        ## Create transition->place edges
        for edge in self.arcs_transition_place_:
            node1 = str(self.transition_to_label_[edge[0]])
            node2 = str(self.place_to_label_[edge[1]])
            edge_weight = str(edge[2])
            net.edge(node1, node2, edge_weight, fontsize='12')

        ## Create automaton pdf and open it
        net.render(filename, view=show_output)

    def next_marking(self, u):
        if len(self.incidence_matrix_) == len(u):
            print("Next marking:")
            marking = self.init_marking_ + np.matmul(u,self.incidence_matrix_)
        else:
            print("Incidence matrix not initialized. Returning initial marking:")
            marking = self.init_marking_
        return marking