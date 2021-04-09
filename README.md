# discrete-event-systems-sandbox
This project will implement simple automata utilities for educational purposes.

# How to run the automata script?

Simply go to the [automata](https://github.com/marcos-pereira/discrete-event-systems-sandbox/tree/main/automata) directory and run
```
python3 main.py
```
The code will plot several automata examples including one that obtains the accessible part of one of the automata.

# How to run the petri net script?

Simply go to the [petri_nets](https://github.com/marcos-pereira/discrete-event-systems-sandbox/tree/main/petri_nets) directory and run
```
python3 main.py
```
The code will plot net5 and net5 controlled. The code also contains some examples of controlled and uncontrolled petri nets.

You can also try to run the `main_final_project.py`.
```
python3 main_final_project.py
```

The code will run the timed petri net chosen with the variable `num_net`.

You can set how much time the simulation will run with the variables `run_time`. 
Note that the time evolution of the net is event driven. 
The places were temporized.
The evolution of the net states happens because of the timed petri net time evolution. 
The time passes when a transition becomes timely enabled according to each place required time.

The `frame_time` will set how much time will be spent on each frame plot (so that you can see the evolution of the net states). This time has nothing to do with the net time. It is only for visualization purposes.

Last, the variable `manual_control` will allow to run the net manually, that is, you press enter to see the transition between each transition.