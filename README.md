# busplan

## Installation

Make sure you have python installed on your computer, then simply use `git pull`

## Running


### Solver

`solver.py` parses inputs from `./all_inputs` and writes outputs to `./output_submission/busplan` ONLY IF the solution is better than what is already written in the output file.

Windows: `py solver.py`
UNIX: `python3 solver.py`

Specify an algorithm with an additional variable. eg. `py solver.py BasicFriends`
To view cached score, run `py solver.py None`


### Improver

`localImprove.py` parses outputs from `./output_submission/busplan` and overrides them with better solutions if one is found.

Specify an improving algorithm with the first variable. The number of iterations with another variable. eg. `py localImprove.py consec 10`

`doOne.py` runs local improvement algorithms on one file. eg. `py doOne.py small 1 step 10` runs the corresponding improvement algorithm on `/small/1.out`


### Cache

`dic.pkl` is a dictionary that keeps the best score found for each input, and the method used to find it.


### Helpers

`lookup.py` looks up the current score for an input. eg. `py lookup.py small 1` prints the score of the output in `/small/1.out`

`correct.py` inspects all output files and scores cached in `dic.pkl`, and rewrites `dic.pkl` if any inconsistency is found.


### Utils

`./utils/heap.py` contains an implementation of MinHeap and MaxHeap that helps with some algorithms.
