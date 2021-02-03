#!/usr/bin/env python

import numpy as np
from PetriNet import PetriNet

def main():

    ## Client queue and server net
    net1_places = {'P1','P2','P3'}
    net1_init_marking = np.array([0,0,1])
    net1_incidence_matrix = np.array([[1,0,0],
                                      [-1,1,-1],
                                      [0,-1,1]])
    net1 = PetriNet(net1_places,net1_init_marking,net1_incidence_matrix)
    net1_u1 = np.array([1,0,0])
    print(net1.next_marking(net1_u1))

    ## Machine 1, Robot and Machine 2 net
    net2_places = {'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'}
    net2_init_marking = np.array([0, 0, 0, 0, 1, 1, 1])
    net2_incidence_matrix = np.array([[1, 0, 0, 0, -1, 0, 0],
                                      [-1, 1, 0, 0, 0, 0, 0],
                                      [0, -1, 1, 0, 1, -1, 0],
                                      [0, 0, -1, 1, 0, 1, -1],
                                      [0, 0, 0, -1, 0, 0, 1]])
    net2 = PetriNet(net2_places, net2_init_marking, net2_incidence_matrix)
    net2_u1 = np.array([1, 0, 0, 0, 0])
    print(net2.next_marking(net2_u1))

    ## Machine 1, Robot and Machine 2 net with Aminus Aplus
    net3_places = {'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'}
    net3_init_marking = np.array([0, 0, 0, 0, 1, 1, 1])
    net3_Aminus = np.array([[0, 0, 0, 0, -1, 0, 0],
                            [-1, 0, 0, 0, 0, 0, 0],
                            [0, -1, 0, 0, 0, -1, 0],
                            [0, 0, -1, 0, 0, 0, -1],
                            [0, 0, 0, -1, 0, 0, 0]])
    net3_Aplus = np.array([[1, 0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0, 0],
                           [0, 0, 1, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 1, 0],
                           [0, 0, 0, 0, 0, 0, 1]])
    net3 = PetriNet.split_incidence_matrix(net3_places, net3_init_marking, net3_Aminus, net3_Aplus)
    net3_u1 = np.array([1, 0, 0, 0, 0])
    print(net3.next_marking(net3_u1))

if __name__ == '__main__':

    main()