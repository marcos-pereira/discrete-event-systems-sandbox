#!/usr/bin/env python

import numpy as np
from PetriNet import PetriNet

def main():

    ## Show output of plotting net
    show_output = True

    ## TASK 2
    net5_places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
    net5_transitions = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
    net5_init_marking = np.array([3, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    net5_tokens_type = ['red','green','blue']
    net5_places_tokens = [['red','green','blue'],[],['red','green','blue'],[],[],[],[],[],[],[]]
    net5_tokens_sequence = ['blue', 'green', 'red']
    net5_logic_transitions = [('t1','count'), ('t5','choice'), ('t6','choice'), ('t7','choice'), ('t8','reset_count')]
    net5_transitions_logic = [lambda token_num: 'blue' if token_num == 0 else ('green' if token_num == 1 else 'red'),
                              lambda token_type: 't5' if token_type == 'red' else ('t6' if token_type == 'green' else 't7'),
                              lambda token_type: 't5' if token_type == 'red' else ('t6' if token_type == 'green' else 't7'),
                              lambda token_type: 't5' if token_type == 'red' else ('t6' if token_type == 'green' else 't7')]
    net5_incidence_matrix = np.array([[-1, 1, -1, 0, 0, 0, 0, 0, 0, 0],
                                      [0, -1, 1, 0, 0, 0, 0, 0, 1, 0],
                                      [0, 0, -1, 0, 0, -1, 1, 0, 0, 0],
                                      [0, 0, 1, 0, 0, 0, -1, 1, 0, 1],
                                      [0, 0, 0, 0, 0, 1, 0, 0, -1, 0],
                                      [0, 0, 0, 0, 1, 0, 0, 0, -1, 1],
                                      [0, 0, 0, 1, 0, 0, 0, 0, -1, 1],
                                      [3, 0, 0, 0, 0, 0, 0, 0, 0, -3]])
    net5 = PetriNet(net5_places, net5_transitions, net5_init_marking)
    net5.set_incidence_matrix(net5_incidence_matrix)
    net5.set_arcs_incidence_matrix()
    net5.set_tokens_type(net5_tokens_type)
    net5.set_places_tokens(net5_places_tokens)
    net5.set_tokens_sequence(net5_tokens_sequence)
    net5.set_logic_transitions(net5_logic_transitions)
    net5.set_transitions_logic(net5_transitions_logic)
    net5.plot('net5', True)
    net5.run_conditional_timed_net()

if __name__ == '__main__':

    main()