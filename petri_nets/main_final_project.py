#!/usr/bin/env python

import numpy as np
from PetriNet import PetriNet
import matplotlib.pyplot as plt

def main():

    ## Show output of plotting net
    show_output = True

    ## TASK 2
    # net5_places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11']
    # net5_transitions = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
    # net5_init_marking = np.array([3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1])
    # net5_tokens_type = ['red','green','blue']
    # p1_t = np.array([[0.0, 0.0, 0.0]])
    # p2_t = np.array([[3.0, 1.0, 5.0]])
    # p3_t = np.array([[0.0, 0.0, 0.0]])
    # p4_t = np.array([[0.0, 0.0, 0.0]])
    # p5_t = np.array([[0.0, 0.0, 0.0]])
    # p6_t = np.array([[0.0, 0.0, 0.0]])
    # p7_t = np.array([[3.0, 0.0, 0.0]])
    # p8_t = np.array([[0.0, 0.0, 0.0]])
    # p9_t = np.array([[1.0, 1.0, 1.0]])
    # p10_t = np.array([[0.0, 0.0, 0.0]])
    # p11_t = np.array([[0.0, 0.0, 0.0]])
    # net5_places_time = np.concatenate((p1_t,p2_t,p3_t,p4_t,p5_t,p6_t,p7_t,p8_t,p9_t,p10_t,p11_t),axis=0)
    # net5_places_time = np.transpose(net5_places_time)
    # print(net5_places_time)
    # net5_places_tokens = [['red','green','blue'],[],['red','green','blue'],[],[],[],[],[],[],[],[]]
    # net5_tokens_sequence = ['blue', 'green', 'red']
    # net5_logic_transitions = [('t1','count'), ('t5','choice'), ('t6','choice'), ('t7','choice'), ('t8','reset_count')]
    # net5_transitions_logic = [lambda token_num: 'blue' if token_num == 0 else ('green' if token_num == 1 else 'red'),
    #                           lambda token_type: 't5' if token_type == 'red' else ('t6' if token_type == 'green' else 't7'),
    #                           lambda token_type: 't5' if token_type == 'red' else ('t6' if token_type == 'green' else 't7'),
    #                           lambda token_type: 't5' if token_type == 'red' else ('t6' if token_type == 'green' else 't7'),
    #                           0]
    # net5_incidence_matrix = np.array([[-1, 1, -1, 0, 0,  0,  0, 0,  0,  0, -1],
    #                                   [0, -1,  1, 0, 0,  0,  0, 0,  1,  0,  0],
    #                                   [0,  0, -1, 0, 0, -1,  1, 0,  0,  0,  0],
    #                                   [0,  0,  1, 0, 0,  0, -1, 1,  0,  1,  0],
    #                                   [0,  0,  0, 0, 0,  1,  0, 0, -1,  0,  1],
    #                                   [0,  0,  0, 0, 1,  0,  0, 0, -1,  1,  1],
    #                                   [0,  0,  0, 1, 0,  0,  0, 0, -1,  1,  1],
    #                                   [3,  0,  0, 0, 0,  0,  0, 0,  0, -3,  0]])
    # net5 = PetriNet(net5_places, net5_transitions, net5_init_marking)
    # net5.set_incidence_matrix(net5_incidence_matrix)
    # net5.set_arcs_incidence_matrix()
    # net5.set_tokens_type(net5_tokens_type)
    # net5.set_places_tokens(net5_places_tokens)
    # net5.set_tokens_sequence(net5_tokens_sequence)
    # net5.set_logic_transitions(net5_logic_transitions)
    # net5.set_transitions_logic(net5_transitions_logic)
    # net5.set_places_time(net5_places_time)
    # net5.plot('net5', True)
    # net5.run_conditional_timed_net()

    net5_places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15']
    net5_transitions = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11']
    net5_init_marking = np.array([3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0])
    p1_t = 0.01 # NUM_OBJ
    p2_t = 5 # ROBOT
    p3_t = 0.1 # ROBOT AVAILABLE
    p4_t = 0 # BOOK
    p5_t = 0 # P1
    p6_t = 2 # HEAT
    p7_t = 5 # ROBOT
    p8_t = 0 # P2
    p9_t = 1 # PLACE
    p10_t = 0.1 # FINISH
    p11_t = 1 # NEXT_OBJ
    p12_t = 1 # BLUE
    p13_t = 1 # GREEN
    p14_t = 1 # RED
    p15_t = 0.5 # OBJ_ENABLED
    net5_places_time = np.array([p1_t, p2_t, p3_t, p4_t, p5_t, p6_t, p7_t, p8_t, p9_t, p10_t, p11_t, p12_t, p13_t, p14_t, p15_t])
    print(net5_places_time)
    net5_incidence_matrix = np.array([[-1, 1, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, -1],
                                      [0, -1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                      [0, 0, -1, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 1, 0, 0, 0, -1, 1, 0, 1, 1, 2, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 1, 0, 0, -2, 0, 0, 0, 0, -1, 0],
                                      [0, 0, 0, 0, 1, 0, 0, 0, -2, 1, 1, 0, -1, 3, 0],
                                      [0, 0, 0, 1, 0, 0, 0, 0, -2, 1, 1, -1, 3, 0, 0],
                                      [3, 0, 0, 0, 0, 0, 0, 0, 0, -3, 0, 2, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -3, 0, 0, 1],
                                      [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -2, 0, 1],
                                      [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -2, 1]])
    net5 = PetriNet(net5_places, net5_transitions, net5_init_marking)
    net5.set_incidence_matrix(net5_incidence_matrix)
    net5.set_arcs_incidence_matrix()
    net5.set_places_time(net5_places_time)
    net5.plot('net5', True)
    # Run time for petri net (s)
    run_time = 100
    # Frame time (s)
    frame_time = 0.0
    manual_control = False
    net_markings, sim_time = net5.run_timed_net(run_time, frame_time, show_output, manual_control)

    # Plot num objects in place 4 (books)
    plt.plot(sim_time[:], net_markings[:, 3], 'b-')
    # Plot num objects in place 5 (salads)
    plt.plot(sim_time[:], net_markings[:, 4], 'g-')
    # Plot num objects in place 8 (meats)
    plt.plot(sim_time[:], net_markings[:, 7], 'r-')
    plt.title('Number of objects')
    plt.ylabel('Number')
    plt.xlabel('Time (s)')
    plt.show()

if __name__ == '__main__':

    main()