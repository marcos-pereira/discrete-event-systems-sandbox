import numpy as np

class PetriNet:
    def __init__(self, places, init_marking, incidence_matrix):
        self.places_ = places
        self.init_marking_ = init_marking
        self.incidence_matrix_ = incidence_matrix

    def next_marking(self, u):
        marking = self.init_marking_ + np.matmul(u,self.incidence_matrix_)
        return marking
