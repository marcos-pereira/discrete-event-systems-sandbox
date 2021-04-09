#!/usr/bin/env python

import numpy as np
from PetriNet import PetriNet

def main():

    ## Show output of plotting net
    show_output = False

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
    net3.enabled_transitions()
    # net3.run_net()
    [net3_transitions_fired, net3_markings] = net3.run_net_randomly(20)
    print("Net3 transitions fired:")
    print(net3_transitions_fired)
    print("Net3 markings:")
    for net3_marking in net3_markings:
        print(net3_marking)

    ## Petri net example based on incidence matrix and resulting control
    net4_places = ['P1', 'P2']
    net4_transitions = ['t1', 't2', 't3', 't4']
    net4_init_marking = np.array([0, 1])
    net4_incidence_matrix = np.array([[1, 0],
                                      [-1, 0],
                                      [0, 1],
                                      [0, -1]])
    net4 = PetriNet(net4_places, net4_transitions, net4_init_marking)
    net4.set_incidence_matrix(net4_incidence_matrix)
    net4.set_arcs_incidence_matrix()
    net4_constraints_matrix = np.array([[1],
                                        [-1]])
    net4_constraints_vector = np.array([-1])
    net4.plot('net4', False)
    net4.control_net(net4_constraints_matrix, net4_constraints_vector)
    net4.set_arcs_incidence_matrix()
    net4.plot('net4_controlled', False)

    ## Petri net example based on incidence matrix and resulting control
    net5_places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
    net5_transitions = ['t1', 't2', 't3', 't4', 't5']
    net5_init_marking = np.array([0, 0, 0, 1, 4, 4])
    net5_incidence_matrix = np.array([[1, 0, 0, 0, -1, 0],
                                      [0, 1, 0, 0, 0, -1],
                                      [-1, 0, 1, -1, 1, 0],
                                      [0, -1, 1, -1, 0, 1],
                                      [0, 0, -1, 1, 0, 0]])
    net5 = PetriNet(net5_places, net5_transitions, net5_init_marking)
    net5.set_incidence_matrix(net5_incidence_matrix)
    net5.set_arcs_incidence_matrix()
    net5_constraints_matrix = np.array([[1],
                                        [1],
                                        [1],
                                        [0],
                                        [0],
                                        [0]])
    net5_constraints_vector = np.array([8])
    net5.plot('net5', True)
    net5.control_net(net5_constraints_matrix, net5_constraints_vector)
    net5.set_arcs_incidence_matrix()
    net5.plot('net5_controlled', True)

if __name__ == '__main__':

    main()