import networkx as nx
import pickle
import random
import os

from utils.heap import MaxHeap, MinHeap
from clear import save_dic, load_dic

from solver import *


def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''

    bestSoFar = load_dic()

    improved = 0

    # for directory in ['medium']:
    #     subfolders = [x[1] for x in os.walk(path_to_inputs + '/' + directory)][0]
    #     for subfolder in subfolders:
    directory = 'large'
    subfolder = '1000'

    path = path_to_inputs + '/' + directory + '/' + subfolder
    graph, num_buses, size_bus, constraints = parse_input(path)
    print(directory + ' ' + subfolder)

    solve = solve_basicFriends

    solution = solve(graph.copy(), num_buses, size_bus, constraints)
    localScore = calc_LocalScore(graph, constraints, solution[0], size_bus)

    print(solution[0])
    print(solution[1])
    print(localScore)


    # if (solution[1] > bestSoFar[directory][subfolder]['score']):
    #     print('Improved ' + directory + ' ' + subfolder + ' by ' + str(solution[1] - bestSoFar[directory][subfolder]['score']))
    #     improved += 1
    #
    # print('improved: ' + str(improved))
    # graph, num_buses, size_bus, constraints = parse_input("testInputs/input1")
    # solution = solve(graph, num_buses, size_bus, constraints)
    # output_file = open("testOutputs/output1/output1.out", "w")
    #
    # for bus in solution:
    #     output_file.write(str(bus) + '\n')
    # output_file.close()

if __name__ == '__main__':
    main()
