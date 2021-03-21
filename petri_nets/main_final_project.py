#!/usr/bin/env python

import numpy as np
from PetriNet import PetriNet

def main():

    ## Show output of plotting net
    show_output = True

    ## TASK 2
    net5_places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']
    net5_transitions = ['t1', 't2', 't3']
    net5_init_marking = np.array([4, 0, 1, 0, 0, 0, 0])
    net5_incidence_matrix = np.array([[-1, 1, -1, 0, 0, 0, 0],
                                      [0, -1, 1, 1, 1, 1, 0],
                                      [0, 0, 1, 0, 0, -1, 1]])
    net5 = PetriNet(net5_places, net5_transitions, net5_init_marking)
    net5.set_incidence_matrix(net5_incidence_matrix)
    net5.set_arcs_incidence_matrix()
    net5.plot('net5', True)

if __name__ == '__main__':

    main()