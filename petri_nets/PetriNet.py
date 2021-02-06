import numpy as np

class PetriNet:

    incidence_matrix_ = np.array([])
    arcs_ = set()
    arcs_place_transition = set()
    arcs_transition_place = set()

    def __init__(self, places, init_marking, Aminus = np.array([]), Aplus = np.array([])):
        self.places_ = places
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
                        arc = (place+1, transition+1, abs(self.Aminus_[transition, place]))
                        self.arcs_.add(arc)
                        self.arcs_place_transition.add(arc)

            ## Add arcs from transitions to places
            num_rows_Aplus = np.shape(self.Aplus_)[0]
            num_cols_Aplus = np.shape(self.Aplus_)[1]
            for transition in range(num_rows_Aplus):
                for place in range(num_cols_Aplus):
                    # Add arc place, transition and weight if arc weight is nonzero
                    if self.Aplus_[transition,place] != 0:
                        arc = (transition+1, place+1, abs(self.Aplus_[transition, place]))
                        self.arcs_.add(arc)
                        self.arcs_transition_place.add(arc)

        else:
            print("Arcs not being set because Aminus and Aplus are not set")

    def print(self):
        print("Places:")
        print(self.places_)

        print("Initial marking:")
        print(self.init_marking_)

        print("Aminus:")
        print(self.Aminus_)

        print("Aplus:")
        print(self.Aplus_)

        print("Arcs:")
        print(self.arcs_)

        print("Arcs (place,transition):")
        print(self.arcs_place_transition)

        print("Arcs (transition, place):")
        print(self.arcs_transition_place)

        print("Incidence matrix:")
        print(self.incidence_matrix_)

    def next_marking(self, u):
        if len(self.incidence_matrix_) == len(u):
            print("Next marking:")
            marking = self.init_marking_ + np.matmul(u,self.incidence_matrix_)
        else:
            print("Incidence matrix not initialized. Returning initial marking:")
            marking = self.init_marking_
        return marking