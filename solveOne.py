import networkx as nx
import pickle
import random
import os
import sys

from clear import save_dic, load_dic
from utils.heap import MaxHeap, MinHeap
from solver import *

###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "./output_submission/busplan"

total_inputs = 722

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''

    bestSoFar = load_dic()
    total = 0
    improved = 0

    directory = sys.argv[1]
    subfolder = sys.argv[2]

    if len(sys.argv) > 3:
        method = sys.argv[3]

    if method == 'fastOrderFill':
        solve = solve_fastOrderFill
    elif method == 'fastOrder':
        solve = solve_fastOrder
    elif method == 'revOrderFill':
        solve = solve_revOrderFill
    elif method == 'random':
        solve = solve_random
    elif method == 'naiveFriends':
        solve = solve_naiveFriends
    elif method == 'basicFriends':
        solve = solve_basicFriends
    elif method == 'maxFriends':
        solve = solve_maxFriends
    elif method == 'friendsFill':
        solve = solve_friendsFill

    if method == 'None':
        return

    path = path_to_inputs + '/' + directory + '/' + subfolder
    graph, num_buses, size_bus, constraints = parse_input(path)

    if method in ['fastOrderFill', 'fastOrder', 'revOrderFill', 'naiveFriends', 'basicFriends']:
        if bestSoFar[directory][subfolder]['method'] == method:
            print('Same deterministic result. Skipped.')
            return


    solution = solve(graph.copy(), num_buses, size_bus, constraints)

    if (solution[1] >= bestSoFar[directory][subfolder]['score']):
        print('Improved ' + directory + ' ' + subfolder + ' by ' + str(solution[1] - bestSoFar[directory][subfolder]['score']))
        bestSoFar[directory][subfolder]['score'] = solution[1]
        bestSoFar[directory][subfolder]['method'] = method

        output_file = open(path_to_outputs + '/' + directory + '/' + subfolder + '.out', 'w+')
        for bus in solution[0]:
            output_file.write(str(bus) + '\n')
        output_file.close()
        save_dic(bestSoFar)

    else:
        print('No improvement on ' + directory + ' ' + subfolder)

    save_dic(bestSoFar)


if __name__ == '__main__':
    main()
