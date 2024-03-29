# Discrete event systems final project at Universidade Federal de Minas Gerais (UFMG)
# Author: Marcos da Silva Pereira 2020740723
# Email: marcos.si.pereira@gmail.com ; marcos-si-pereira@ufmg.br
# Last modified: 26.03.2021

import numpy as np
import random
from graphviz import Digraph
import time

class PetriNet:

    def __init__(self,
                 places,
                 transitions,
                 init_marking,
                 Aminus = np.array([]),
                 Aplus = np.array([]),
                 incidence_matrix = np.array([])):
        # Create some class instance variables
        self.incidence_matrix_ = np.array([])
        self.marking_ = np.array([])
        self.places_time = np.array([])
        self.tokens_type_ = list()
        self.tokens_sequence_ = list()
        self.places_tokens = list(list())
        self.token_to_label_ = dict()
        self.label_to_token_ = dict()
        self.logic_transitions_ = list()
        self.transitions_logic_ = list()
        self.arcs_ = set()
        self.arcs_place_transition_ = set()
        self.arcs_transition_place_ = set()
        self.place_to_label_ = dict()
        self.label_to_place_ = dict()
        self.transition_to_label_ = dict()
        self.label_to_transition_ = dict()

        self.places_ = places.copy()
        for place_num in range(len(self.places_)):
            self.label_to_place_[places[place_num]] = place_num
            self.place_to_label_[place_num] = places[place_num]
        self.transitions_ = transitions.copy()
        for transition_num in range(len(self.transitions_)):
            self.label_to_transition_[transitions[transition_num]] = transition_num
            self.transition_to_label_[transition_num] = transitions[transition_num]
        self.init_marking_ = init_marking.copy()
        self.marking_ = init_marking.copy()
        self.Aminus_ = Aminus.copy()
        self.Aplus_ = Aplus.copy()
        if len(incidence_matrix != 0):
            self.incidence_matrix_ = incidence_matrix.copy()
        else:
            self.incidence_matrix_ = Aminus + Aplus

    def set_incidence_matrix(self, incidence_matrix):
        self.incidence_matrix_ = incidence_matrix

    def set_arcs_Aminus_Aplus(self):
        if len(self.Aminus_) !=0 and len(self.Aminus_) != 0:
            ## Add arcs from places to transitions
            num_rows_Aminus = np.shape(self.Aminus_)[0]
            num_cols_Aminus = np.shape(self.Aminus_)[1]
            for transition in range(num_rows_Aminus):
                for place in range(num_cols_Aminus):
                    # Add arc place, transition and weight if arc weight is nonzero
                    if self.Aminus_[transition, place] != 0:
                        arc = (place, transition, abs(self.Aminus_[transition, place]))
                        self.arcs_.add(arc)
                        self.arcs_place_transition_.add(arc)

            ## Add arcs from transitions to places
            num_rows_Aplus = np.shape(self.Aplus_)[0]
            num_cols_Aplus = np.shape(self.Aplus_)[1]
            for transition in range(num_rows_Aplus):
                for place in range(num_cols_Aplus):
                    # Add arc transition, place and weight if arc weight is nonzero
                    if self.Aplus_[transition,place] != 0:
                        arc = (transition, place, abs(self.Aplus_[transition, place]))
                        self.arcs_.add(arc)
                        self.arcs_transition_place_.add(arc)

        else:
            print("Arcs not being set because Aminus and Aplus are not set")

    def set_arcs_incidence_matrix(self):
        if len(self.incidence_matrix_ != 0):
            A = self.incidence_matrix_
            num_rows_A = np.shape(A)[0]
            num_cols_A = np.shape(A)[1]
            ## Iterate through incidence matrix
            for transition in range(num_rows_A):
                for place in range(num_cols_A):
                    # If number is negative, add an arc from place to transition
                    # That is, the transition consumes tokens from the place
                    if A[transition,place] < 0:
                        arc = (place, transition, abs(A[transition,place]))
                        self.arcs_.add(arc)
                        self.arcs_place_transition_.add(arc)
                    # If number is positive, add an arc from transition to place
                    # That is, the transition add tokens to the place
                    elif A[transition,place] > 0:
                        arc = (transition, place, abs(A[transition,place]))
                        self.arcs_.add(arc)
                        self.arcs_transition_place_.add(arc)
        else:
            print("Incidence matrix not set")

    def set_tokens_type(self,tokens_type):
        self.tokens_type_ = tokens_type.copy()
        for token_num in range(len(self.tokens_type_)):
            self.label_to_token_[self.tokens_type_[token_num]] = token_num
            self.token_to_label_[token_num] = self.tokens_type_[token_num]

    def set_places_tokens(self,places_tokens):
        self.places_tokens = places_tokens.copy()

    def set_logic_transitions(self, logic_transitions):
        self.logic_transitions_ = logic_transitions.copy()

    def set_tokens_sequence(self, tokens_sequence):
        self.tokens_sequence_ = tokens_sequence.copy()

    def set_transitions_logic(self, transitions_logic):
        self.transitions_logic_ = transitions_logic.copy()

    def set_places_time(self, places_time):
        self.places_time = places_time.copy()

    def print(self):
        print("Places:")
        print(self.places_)

        print("Transitions:")
        print(self.transitions_)

        print("Initial marking:")
        print(self.init_marking_)

        print("Aminus:")
        print(self.Aminus_)

        print("Aplus:")
        print(self.Aplus_)

        print("Arcs:")
        print(self.arcs_)

        print("Arcs (place,transition):")
        print(self.arcs_place_transition_)

        print("Arcs (transition, place):")
        print(self.arcs_transition_place_)

        print("Incidence matrix:")
        print(self.incidence_matrix_)

    def plot(self, filename, show_output):

        ## Create graph
        net = Digraph(comment=filename)

        ## Print horizontally
        net.attr(rankdir='LR', size='8.5')

        ## Create net places
        for place in self.places_:
            place_label = place
            if self.marking_[self.label_to_place_[place]] != 0:
                place_marking = str(self.marking_[self.label_to_place_[place]])
            else:
                place_marking = ""
            net.attr('node', shape='circle', fontsize='12')
            net.node(place, label=place_marking, xlabel=place_label)

        ## Create net transitions
        for transition in self.transitions_:
            transition_label = transition
            net.attr('node', shape='square', fontsize='12')
            net.node(transition, label="", xlabel=transition_label)

        ## Create place->transition edges
        for edge in self.arcs_place_transition_:
            node1 = str(self.place_to_label_[edge[0]])
            node2 = str(self.transition_to_label_[edge[1]])
            edge_weight = str(edge[2])
            # If edge weight equals 1, do not plot 1 to make drawing clearer
            if edge[2] == 1:
                net.edge(node1, node2)
            else:
                net.edge(node1, node2, edge_weight)

        ## Create transition->place edges
        for edge in self.arcs_transition_place_:
            node1 = str(self.transition_to_label_[edge[0]])
            node2 = str(self.place_to_label_[edge[1]])
            edge_weight = str(edge[2])
            # If edge weight equals 1, do not plot 1 to make drawing clearer
            if edge[2] == 1:
                net.edge(node1, node2)
            else:
                net.edge(node1, node2, edge_weight, fontsize='12')

        ## Create net pdf and open it
        net.render(filename, view=show_output)

    def next_marking(self, u):
        print("Input u:")
        print(u)
        # If incidence matrix is initialized
        if len(self.incidence_matrix_) == len(u):
            # Fire transition and get new marking
            marking = self.marking_ + np.matmul(u,self.incidence_matrix_)
        else:
            print("Incidence matrix not initialized. Returning initial marking:")
            marking = self.init_marking_
        self.marking_ = marking
        print("Next marking:")
        print(self.marking_)
        return marking

    def next_marking_manually(self, u, marking):
        print("Input u:")
        print(u)
        # If incidence matrix is initialized
        if len(self.incidence_matrix_) == len(u):
            # Fire transition and get new marking
            next_marking = marking + np.matmul(u,self.incidence_matrix_)
        else:
            print("Incidence matrix not initialized. Returning initial marking:")
            next_marking = self.init_marking_
        print("Next marking manually:")
        print(next_marking)
        return next_marking

    def enabled_transitions(self):
        enabled_transitions = set()
        for transition in self.transitions_:
            ## Assume transition starts enabled
            transition_enabled = True
            ## Get corresponding input edges to transition
            for arc in self.arcs_place_transition_:
                arc_place = arc[0]
                arc_transition = arc[1]
                arc_weight = arc[2]
                ## If arc transition corresponds to the transition
                if arc_transition == self.label_to_transition_[transition]:
                    ## Check for all places that have edges input to the transition
                    # if the place marking is lower than the arc_weight
                    for place in range(len(self.marking_)):
                        if place == arc_place:
                            if self.marking_[place] < arc_weight:
                                transition_enabled = False

            if transition_enabled == True:
                enabled_transitions.add(transition)

        return enabled_transitions

    def run_net(self):
        transition_to_fire = ''
        while True:
            print("-----------------------------------")
            if transition_to_fire == "exit":
                break
            print("Transitions labels:")
            print(self.transitions_)
            print("Enabled transitions:")
            print(self.enabled_transitions())
            print("Enter transition to fire:")
            transition_to_fire = input()
            # If transition label is wrong, ask for new transition label
            if transition_to_fire not in self.transitions_ or transition_to_fire not in self.enabled_transitions():
                print("Wrong transition label or transition not enabled!")
            else:
                print("Transition number:")
                transition_number = self.label_to_transition_[transition_to_fire]
                print(transition_number)

                # Initialize input vector with zeros
                u = np.zeros(len(self.transitions_))
                # Make respective transition equals 1 to fire it
                u[transition_number] = 1
                print("Input vector:")
                print(u)

                # Run net after firing transition
                self.next_marking(u)

                self.plot("net_state",True)

    def timed_enabled_transitions(self, places_time, transitions_time):
        enabled_transitions = set()

        # Create a dict of list because every transition can have more than one place
        transitions_to_input_places = dict()

        for transition in self.transitions_:
            transition_num = self.label_to_transition_[transition]
            # Store the time of the places before a transition
            time_places_before_transition = list()
            ## Assume transition starts enabled
            transition_enabled = True
            ## Get corresponding input edges to transition
            for arc in self.arcs_place_transition_:
                arc_place = arc[0]
                arc_transition = arc[1]
                arc_weight = arc[2]
                ## If arc transition corresponds to the transition
                if arc_transition == self.label_to_transition_[transition]:
                    # Places with arcs to a given transition
                    input_places_to_transition = list()
                    ## Check for all places that have edges input to the transition
                    # if the place marking is lower than the arc_weight
                    for place in self.places_:
                        place_num = self.label_to_place_[place]
                        if place_num == arc_place:
                            # A transition may have many input places
                            input_places_to_transition.append(place_num)
                            # Store the time of the place
                            time_places_before_transition.append(places_time[place_num])
                            if self.marking_[place_num] < arc_weight:
                                transition_enabled = False
                    # Map transition to input places of the transition
                    transitions_to_input_places[transition_num] = input_places_to_transition

            # The transition time is the time of the place with the max waiting time
            transitions_time[transition_num] = max(time_places_before_transition)

            if transition_enabled == True:
                # Add transition to enabled transitions
                enabled_transitions.add(transition)


        return enabled_transitions, transitions_time, transitions_to_input_places

    def run_timed_net(self, run_time, frame_time, plot_net, manual_control):
        transition_to_fire = ''
        current_places_time = self.places_time.copy()
        current_transitions_time = np.zeros((len(self.transitions_)))

        for transition in self.transitions_:
            transition_num = self.label_to_transition_[transition]
            # Store the time of the places before a transition
            time_places_before_transition = list()
            ## Get corresponding input edges to transition
            for arc in self.arcs_place_transition_:
                arc_place = arc[0]
                arc_transition = arc[1]
                ## If arc transition corresponds to the transition
                if arc_transition == self.label_to_transition_[transition]:
                    ## Check for all places that have edges input to the transition
                    for place in self.places_:
                        place_num = self.label_to_place_[place]
                        if place_num == arc_place:
                            # Store the time of the place
                            time_places_before_transition.append(self.places_time[place_num])

            # Set transition time to time of place with max time
            current_transitions_time[transition_num] = max(time_places_before_transition)

        # Running time of the net
        net_time = 0

        # Last fired transition time
        last_fired_transition_time = 0

        # Marking of net for the whole run_time
        net_markings = np.zeros((len(self.marking_)))

        # Simulation time
        sim_time = np.array([net_time])

        while net_time < run_time:
            print("-----------------------------------")

            if transition_to_fire == "exit":
                break

            print("Transitions labels:")
            print(self.transitions_)

            print("Places labels:")
            print(self.places_)

            print("Places time:")
            print(self.places_time)

            print("Net marking:")
            print(self.marking_)

            print("Enabled transitions:")
            enabled_transitions, current_transitions_time, transitions_to_input_places = \
                self.timed_enabled_transitions(self.places_time, current_transitions_time)
            print(enabled_transitions)

            # Transitions times of enabled transitions
            transitions_times = list()

            # Timed enabled transitions
            timed_enabled_transitions = list()

            print("Last fired transition time:")
            print(last_fired_transition_time)

            print("Places current time before updating:")
            print(current_places_time)

            # Places that are enabling any transition
            places_enabling_transitions = np.zeros(len(self.places_))

            # Update places current time
            for transition in self.transitions_:
                transition_num = self.label_to_transition_[transition]
                if transition in enabled_transitions:
                    # print("Transition in enabled transitions: " + transition)
                    # For each input place of the transition
                    for place_num in transitions_to_input_places[transition_num]:
                        # Update time of places before enabled transition
                        current_places_time[place_num] = \
                            current_places_time[place_num] - last_fired_transition_time
                        # print("current_places_time " + str(place_num))
                        # print(current_places_time[place_num])
                        places_enabling_transitions[place_num] = 1
                if transition not in enabled_transitions:
                    # print("Transition not in enabled transitions: " + transition)
                    # For each input place of the transition, reset the time since they are not enabled yet
                    for place_num in transitions_to_input_places[transition_num]:
                        if places_enabling_transitions[place_num] == 0:
                            current_places_time[place_num] = self.places_time[place_num]

            print("Places current time after updating:")
            print(current_places_time)

            enabled_transitions_time = list()

            # Check all enabled transitions places time
            for transition in enabled_transitions:
                # print("Enabled transition " + transition)
                transition_num = self.label_to_transition_[transition]
                enabled_transition = True
                # Check all input places to enabled transition
                for place_num in transitions_to_input_places[transition_num]:
                    if current_places_time[place_num] <= 0.0:
                        # print("Time <= 0")
                        # print("current_places_time " + str(place_num))
                        # print(current_places_time[place_num])
                        # Reset place time
                        current_places_time[place_num] = self.places_time[place_num]
                    else:
                        # print("Time > 0")
                        # print("current_places_time " + str(place_num))
                        enabled_transition = False
                        break
                if enabled_transition == True:
                    # Store timely enabled transitions and its time
                    enabled_transitions_time.append(current_places_time[place_num])
                    timed_enabled_transitions.append(transition)
                # Store time of enabled transitions anyway because they will be used to count net time
                transitions_times.append(current_transitions_time[transition_num])

            print("Timed enabled transitions:")
            print(timed_enabled_transitions)

            print("Places current time after resetting:")
            print(current_places_time)

            if len(timed_enabled_transitions) > 0:
                minimum_time_transition = enabled_transitions_time.index(min(enabled_transitions_time))
                transition_to_fire = timed_enabled_transitions[minimum_time_transition]
                print("Transition timely enabled:")
                print(transition_to_fire)
            else:
                last_fired_transition_time = min(transitions_times)
                net_time = net_time + min(transitions_times)
                print("Net time:")
                print(net_time)
                sim_time = np.concatenate([sim_time, [net_time]], axis=0)
                net_markings = np.vstack((net_markings, self.marking_))
                print("No transition timely enabled! Continue...")
                if manual_control == True:
                    print("Press enter to continue")
                    transition_to_fire_manual = input()
                continue

            if manual_control == True:
                print("Enter transition to fire:")
                transition_to_fire_manual = input()
                if transition_to_fire_manual == transition_to_fire:
                    transition_to_fire = transition_to_fire_manual
                else:
                    print("Transition is not timely enabled!")
                    print("Firing transition:")
                    print((transition_to_fire))

            last_fired_transition_time = current_transitions_time[self.label_to_transition_[transition_to_fire]]

            # If transition label is wrong, ask for new transition label
            if transition_to_fire not in self.transitions_ or transition_to_fire not in enabled_transitions:
                print("Wrong transition label or transition not enabled!")
            else:
                print("Transition number:")
                transition_number = self.label_to_transition_[transition_to_fire]
                print(transition_number)

                # Initialize input vector with zeros
                u = np.zeros(len(self.transitions_))
                # Make respective transition equals 1 to fire it
                u[transition_number] = 1
                print("Input vector:")
                print(u)

                # Run net after firing transition
                self.next_marking(u)

                # print("Enabled transitions:")
                # print(enabled_transitions)
                print("Places current time:")
                print(current_places_time)
                print("Transitions current time:")
                print(current_transitions_time)
                print("Enabled transitions time:")
                print(transitions_times)
                print("Transition to fire:")
                print(transition_to_fire)

                self.plot("net_state", plot_net)
                time.sleep(frame_time)

                net_markings = np.vstack((net_markings, self.marking_))

            net_time = net_time + min(transitions_times)
            print("Net time:")
            print(net_time)
            sim_time = np.concatenate([sim_time, [net_time]], axis=0)

        return net_markings, sim_time

    def run_conditional_timed_net(self):
        transition_to_fire = ''

        # Element 0: token type
        # Element 1: token number
        token = tuple()

        # Count the number of times a transition has been fired
        transitions_firing_num = np.zeros(len(self.transitions_))

        # Each row contain the place where the token of a given type is located
        # Each column corresponds to a place
        tokens_matrix = np.zeros((len(self.tokens_type_),len(self.places_)))

        # Initialize tokens matrix
        for place in self.places_:
            place_num = self.label_to_place_[place]
            for token_in_place in self.places_tokens[place_num]:
                token_num = self.label_to_token_[token_in_place]
                tokens_matrix[token_num][place_num] = 1.0

        # Time instants when each place receives its k-th token
        # places_current_time = self.places_time.copy()
        places_current_time = np.zeros((len(self.tokens_type_),len(self.places_)))

        # Time instant of the k-th firing of each transition
        transitions_current_time = np.zeros((len(self.tokens_type_),len(self.transitions_)))

        # Update current time of each transition
        for transition in self.transitions_:
            transition_num = self.label_to_transition_[transition]
            ## Get corresponding place before transition
            for arc in self.arcs_place_transition_:
                arc_place = arc[0]
                arc_transition = arc[1]
                ## If arc transition corresponds to the transition
                if arc_transition == transition_num:
                    for token_type in self.tokens_type_:
                        token_num = self.label_to_token_[token_type]
                        transitions_current_time[token_num][transition_num] = self.places_time[token_num][arc_place]

        # Time of last fired transition
        last_fired_transition_time = 0

        # Net current time
        net_time = 0

        while True:
            print("-----------------------------------")
            if transition_to_fire == "exit":
                break
            print("Transitions labels:")
            print(self.transitions_)
            print("Enabled transitions:")
            print(self.enabled_transitions())
            enabled_transitions = self.enabled_transitions()
            print("Enter transition to fire:")
            transition_to_fire = input()
            # If transition label is wrong, ask for new transition label
            if transition_to_fire not in self.transitions_ or transition_to_fire not in self.enabled_transitions():
                print("Wrong transition label or transition not enabled!")
            else:
                print("Transition number:")
                transition_number = self.label_to_transition_[transition_to_fire]
                print(transition_number)

                # Initialize input vector with zeros
                u = np.zeros(len(self.transitions_))
                # Make respective transition equals 1 to fire it
                u[transition_number] = 1
                print("Input vector:")
                print(u)

                # Apply transitions logic if any
                logic_transitions = [transition[0] for transition in self.logic_transitions_]
                print(logic_transitions)
                if transition_to_fire in logic_transitions:
                    # Get index of logic transition being fired
                    for logic_transition in self.logic_transitions_:
                        if logic_transition[0] == transition_to_fire:
                            logic_transition_index = self.logic_transitions_.index(logic_transition)
                    # If the transition condition is of a count type, use the number of firings the transition had
                    if self.logic_transitions_[logic_transition_index][1] == 'count':
                        # Get logic of transition as a lambda function: get token type based on the number of times the transition fired
                        transition_condition = self.transitions_logic_[transition_number](transitions_firing_num[transition_number])
                        print("Transition_condition:")
                        print(transition_condition)
                        token_type = transition_condition
                        token_num = self.label_to_token_[token_type]
                        # This token will be the same until the next time this transition fires
                        token = (token_type, token_num)

                        # Run net for the given token type
                        print("Tokens matrix before firing:")
                        print(tokens_matrix)
                        next_marking = self.next_marking_manually(u, tokens_matrix[token_num])
                        tokens_matrix[token_num] = next_marking
                        print("Tokens matrix after firing:")
                        print(tokens_matrix)

                    if self.logic_transitions_[logic_transition_index][1] == 'reset_count':
                        # Each row contain the place where the token of a given type is located
                        # Each column corresponds to a place
                        tokens_matrix = np.zeros((len(self.tokens_type_), len(self.places_)))

                        # Reset tokens matrix
                        for place in self.places_:
                            place_num = self.label_to_place_[place]
                            for token in self.places_tokens[place_num]:
                                token_num = self.label_to_token_[token]
                                tokens_matrix[token_num][place_num] = 1.0

                        # Reset places current time
                        places_current_time = np.zeros((len(self.tokens_type_), len(self.places_)))

                        # Reset token
                        token =(self.tokens_type_[0], self.label_to_token_[self.tokens_type_[0]])

                    # If the transition is of a choice type, use the type of token
                    if self.logic_transitions_[logic_transition_index][1] == 'choice':
                        ## Get corresponding place before choice transition
                        for arc in self.arcs_place_transition_:
                            arc_place = arc[0]
                            arc_transition = arc[1]
                            ## If arc transition corresponds to the transition
                            if arc_transition == transition_number:
                                for token_type in self.tokens_type_:
                                    token_num = self.label_to_token_[token_type]
                                    # print(token_type)
                                    # print(token_num)
                                    # print(tokens_matrix[token_num][arc_place])
                                    if tokens_matrix[token_num][arc_place] == 1.0:
                                        place_token_type = token_type
                                        place_token_num = self.label_to_token_[place_token_type]
                                        break # token type found
                                # Get logic of transition as a lambda function: get transition based on the place token type
                                transition_condition = self.transitions_logic_[logic_transition_index](place_token_type)
                                print("Transition_condition:")
                                print(transition_condition)
                                break  # transition found

                        # Update transition to fire considering condition
                        transition_to_fire = transition_condition
                        transition_number = self.label_to_transition_[transition_to_fire]

                        # Update enabled transitions based on condition
                        enabled_transitions = {transition_to_fire}

                        if transition_to_fire != transition_condition:
                            print("Transition not enabled due to transition condition!")
                            continue

                        print("Transition to be fired due to transition condition:")
                        print(transition_to_fire)
                        # Initialize input vector with zeros
                        u = np.zeros(len(self.transitions_))
                        # Make respective transition equals 1 to fire it
                        u[transition_number] = 1
                        print("Input vector:")
                        print(u)

                        # Run net for the given token type
                        print("Tokens matrix before firing:")
                        print(tokens_matrix)
                        next_marking = self.next_marking_manually(u, tokens_matrix[place_token_num])
                        tokens_matrix[token_num] = next_marking
                        print("Tokens matrix after firing:")
                        print(tokens_matrix)

                else:
                    # Run net for the given token type
                    print("Tokens matrix before firing:")
                    print(tokens_matrix)
                    # token determined on first transition
                    next_marking = self.next_marking_manually(u, tokens_matrix[token[1]])
                    tokens_matrix[token_num] = next_marking
                    print("Tokens matrix after firing:")
                    print(tokens_matrix)

                # Update number of firings
                transitions_firing_num[transition_number] += 1

                places_without_0 = [place for place in self.places_ if self.label_to_place_[place] != 0]
                for place in places_without_0:
                    place_num = self.label_to_place_[place]
                    for token_type in self.tokens_type_:
                        token_num = self.label_to_token_[token_type]
                        places_current_time[token_num][place_num] = places_current_time[token_num][place_num-1] + \
                                                                    self.places_time[token_num][place_num-1]
                print("Places current time:")
                print(places_current_time)

                enabled_transitions_places = list()

                for place in self.places_:
                    place_num = self.label_to_place_[place]
                    for token_type in self.tokens_type_:
                        token_num = self.label_to_token_[token_type]
                        for arc in self.arcs_place_transition_:
                            arc_place = arc[0]
                            arc_transition = arc[1]
                            ## If arc transition corresponds to the place
                            if arc_place == place_num:
                                transition = self.transition_to_label_[arc_transition]
                                if transition in enabled_transitions:
                                    enabled_transitions_places.append(places_current_time[token[1]][place_num])

                net_time += min(enabled_transitions_places)

                # Update current time of each transition
                # for transition in self.transitions_:
                #     transition_num = self.label_to_transition_[transition]
                #     ## Get corresponding place before transition
                #     for arc in self.arcs_place_transition_:
                #         arc_place = arc[0]
                #         arc_transition = arc[1]
                #         ## If arc transition corresponds to the transition
                #         if arc_transition == transition_num:
                #             if transition in enabled_transitions:
                #                 transitions_current_time[token[1]][transition_num] = transitions_current_time[token[1]][transition_num] - \
                #                                                                      net_time
                #             else:
                #                 transitions_current_time[token[1]][transition_num] = self.places_time[token[1]][arc_place]
                # print("Transitions current time:")
                # print(transitions_current_time)
                # last_fired_transition_time = transitions_current_time[token[1]][transition_number]

                # enabled_transitions_places = list()
                #
                # # Update current time of each place
                # for place in self.places_:
                #     place_num = self.label_to_place_[place]
                #     ## Get corresponding place before transition
                #     for arc in self.arcs_place_transition_:
                #         arc_place = arc[0]
                #         arc_transition = arc[1]
                #         ## If arc transition corresponds to the place
                #         if arc_place == place_num:
                #             transition = self.transition_to_label_[arc_transition]
                #             if transition in enabled_transitions:
                #                 places_current_time[token[1]][place_num] = places_current_time[token[1]][place_num] - \
                #                                                            transitions_current_time[token[1]][arc_transition]
                #                 enabled_transitions_places.append(places_current_time[token[1]][place_num])
                #             else:
                #                 places_current_time[token[1]][place_num] = self.places_time[token[1]][place_num]
                # print("Places current time:")
                # print(places_current_time)

                # net_time += min(enabled_transitions_places)

                print("Net time:")
                print(net_time)

                # Run net after firing transition
                self.next_marking(u)

                self.plot("net_state",True)

    def transition_logic(self,
                         transition_to_fire,
                         transition_number,
                         transitions_firing_num):
        if transition_number == 0:
            transition_condition = self.transitions_logic_[transition_number](transitions_firing_num[transition_number])
        if transition_number == 1:
            transition_condition = self.transitions_logic_[transition_number](transitions_firing_num[transition_number])


    def run_net_randomly(self, num_steps):
        transitions_fired = list()
        markings = list()
        markings.append(self.marking_)
        for step in range(num_steps):
            print("-----------------------------------")
            # Get enabled transitions
            enabled_transitions = self.enabled_transitions()
            # Select randomly transition to fire
            transition_to_fire = random.sample(enabled_transitions,1)[0]
            print("Transition to fire:")
            print(transition_to_fire)
            transitions_fired.append(transition_to_fire)
            transition_number = self.label_to_transition_[transition_to_fire]
            # Initialize input vector with zeros
            u = np.zeros(len(self.transitions_))
            # Make respective transition equals 1 to fire it
            u[transition_number] = 1
            # Ru net after firing transition
            self.next_marking(u)
            markings.append(self.marking_)

        return transitions_fired, markings

    def control_net(self, net_constraints_matrix, net_constraints_vector):
        controller_incidence_matrix = -np.matmul(self.incidence_matrix_,net_constraints_matrix)
        print("Controller incidence matrix:")
        print(controller_incidence_matrix)

        controller_init_marking = net_constraints_vector - np.matmul(self.init_marking_,net_constraints_matrix)
        print("Controller initial marking:")
        print(controller_init_marking)

        complete_incidence_matrix = np.concatenate((self.incidence_matrix_, controller_incidence_matrix), axis=1)
        print("Complete incidence matrix:")
        print(complete_incidence_matrix)

        complete_init_marking = np.concatenate((self.init_marking_, controller_init_marking))
        print("Complete initial marking:")
        print(complete_init_marking)

        # Update incidence matrix
        self.incidence_matrix_ = complete_incidence_matrix

        # Update init marking and marking
        self.init_marking_ = complete_init_marking
        self.marking_ = complete_init_marking

        # Add control places to net places
        for control_place in range(len(controller_init_marking)):
            self.places_.append("C"+str(control_place))

        # Clear dictionaries
        self.label_to_place_ = dict()
        self.place_to_label_ = dict()

        # Update dictionaries
        for place_num in range(len(self.places_)):
            self.label_to_place_[self.places_[place_num]] = place_num
            self.place_to_label_[place_num] = self.places_[place_num]







