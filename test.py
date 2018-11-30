import networkx as nx
import pickle
import random
import os

from utils.heap import MaxHeap, MinHeap
from clear import save_dic, load_dic

from solver import *

def calc_LocalScore(graph, constraints, sol):
    graph = graph.copy()

    for bus in sol:
        if len(bus) == 0:
            return 0

    bus_assignments = {}
    attendance_count = 0

    # make sure each student is in exactly one bus
    attendance = {student:False for student in graph.nodes()}
    for i in range(len(sol)):
        for student in sol[i]:
            attendance[student] = True
            bus_assignments[student] = i

    total_edges = graph.number_of_edges()
    # Remove nodes for rowdy groups which were not broken up
    for i in range(len(constraints)):
        busses = set()
        for student in constraints[i]:
            busses.add(bus_assignments[student])
        if len(busses) <= 1:
            for student in constraints[i]:
                if student in graph:
                    graph.remove_node(student)

    # score output
    score = [0] * len(sol)
    for edge in graph.edges():
        if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
            score[bus_assignments[edge[0]]] += 1
    return score

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
    directory = 'small'
    subfolder = '20'

    path = path_to_inputs + '/' + directory + '/' + subfolder
    graph, num_buses, size_bus, constraints = parse_input(path)
    print(directory + ' ' + subfolder)

    solve = solve_basicFriends

    solution = solve(graph.copy(), num_buses, size_bus, constraints)
    localScore = calc_LocalScore(graph, constraints, solution[0])

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
