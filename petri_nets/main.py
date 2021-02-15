#!/usr/bin/env python

import numpy as np
from PetriNet import PetriNet

def main():

    ## Show output of plotting net
    show_output = True

    ## Client queue and server net
    net1_places = ['P1','P2','P3']
    net1_transitions = ['t1','t2','t3']
    net1_init_marking = np.array([0,0,1])
    net1_incidence_matrix = np.array([[1,0,0],
                                      [-1,1,-1],
                                      [0,-1,1]])
    net1 = PetriNet(net1_places, net1_transitions, net1_init_marking)
    net1.set_incidence_matrix(net1_incidence_matrix)
    net1.set_arcs_Aminus_Aplus()
    # net1.print()
    net1_u1 = np.array([1,0,0])
    print(net1.next_marking(net1_u1))

    ## Machine 1, Robot and Machine 2 net
    net2_places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']
    net2_transitions = ['a1', 'e1', 'd1', 'a2', 'd2']
    net2_init_marking = np.array([0, 0, 0, 0, 1, 1, 1])
    net2_incidence_matrix = np.array([[1, 0, 0, 0, -1, 0, 0],
                                      [-1, 1, 0, 0, 0, 0, 0],
                                      [0, -1, 1, 0, 1, -1, 0],
                                      [0, 0, -1, 1, 0, 1, -1],
                                      [0, 0, 0, -1, 0, 0, 1]])
    net2 = PetriNet(net2_places, net2_transitions, net2_init_marking)
    net2.set_incidence_matrix(net2_incidence_matrix)
    net2.set_arcs_incidence_matrix()
    net2.print()
    net2.plot('net2', show_output)
    net2_u1 = np.array([1, 0, 0, 0, 0])
    print(net2.next_marking(net2_u1))

    ## Machine 1, Robot and Machine 2 net with Aminus Aplus
    net3_places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']
    net3_transitions = ['a1', 'e1', 'd1', 'a2', 'd2']
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
    net3 = PetriNet(net3_places, net3_transitions, net3_init_marking, net3_Aminus, net3_Aplus)
    net3.set_arcs_Aminus_Aplus()
    net3.print()
    net3.plot('net3', show_output)
    net3_u1 = np.array([1, 0, 0, 0, 0])
    net3.next_marking(net3_u1)
    net3.enabled_transitions()

if __name__ == '__main__':

    main()