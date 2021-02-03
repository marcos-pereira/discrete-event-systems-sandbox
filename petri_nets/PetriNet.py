import numpy as np

class PetriNet:
    def __init__(self, places, init_marking, incidence_matrix):
        self.places_ = places
        self.init_marking_ = init_marking
        self.incidence_matrix_ = incidence_matrix

    @classmethod
    def split_incidence_matrix(cls, places, init_marking, Aminus, Aplus):
        incidence_matrix = Aminus+Aplus
        net = cls(places, init_marking, incidence_matrix)
        return net

    @classmethod
    def incidence_matrix(cls, places, init_marking, incidence_matrix):
        net = cls(places, init_marking, incidence_matrix)
        return net


    def next_marking(self, u):
        marking = self.init_marking_ + np.matmul(u,self.incidence_matrix_)
        return marking