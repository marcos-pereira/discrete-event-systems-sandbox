import numpy as np

class PetriNet:

    incidence_matrix_ = np.array([])

    def __init__(self, places, init_marking, Aminus = np.array([]), Aplus = np.array([])):
        self.places_ = places
        self.init_marking_ = init_marking
        self.Aminus_ = Aminus
        self.Aplus_ = Aplus
        self.incidence_matrix_ = Aminus + Aplus

    def set_incidence_matrix(self, incidence_matrix):
        self.incidence_matrix_ = incidence_matrix

    def next_marking(self, u):
        if len(self.incidence_matrix_) == len(u):
            print("Next marking:")
            marking = self.init_marking_ + np.matmul(u,self.incidence_matrix_)
        else:
            print("Incidence matrix not initialized. Returning initial marking:")
            marking = self.init_marking_
        return marking