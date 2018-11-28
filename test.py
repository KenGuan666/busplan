import networkx as nx
import pickle
import random
import os

import queue

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

def save_dic(obj):
    with open('dic.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_dic():
    with open('dic.pkl', 'rb') as f:
        return pickle.load(f)

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints



def solve_naiveFriends(graph, num_buses, size_bus, constraints):

    solution = []
    buses = [[] for i in range(num_buses)]



    score = calcScore(graph.copy(), constraints, solution)
    print(str(score) + '\n')

    return (solution, score)


def solve_fastOrder(graph, num_buses, size_bus, constraints):

    solution = []
    buses = [[] for i in range(num_buses)]

    index = 0
    count = 0
    for n in list(graph.nodes()):
        count += 1
        buses[index].append(n)
        if count == size_bus:
            count = 0
            index += 1
    for b in buses:
        solution.append(b)

    score = calcScore(graph.copy(), constraints, solution)
    print(str(score) + '\n')

    return (solution, score)


def solve_random(graph, num_buses, size_bus, constraints):

    lst = list(graph.nodes())
    random.shuffle(lst)
    solution = fillHelper(lst, num_buses)

    score = calcScore(graph.copy(), constraints, solution)
    print(str(score) + '\n')

    return (solution, score)


def solve_fastOrderFill(graph, num_buses, size_bus, constraints):

    solution = fillHelper(list(graph.nodes()), num_buses)

    score = calcScore(graph.copy(), constraints, solution)
    print(str(score) + '\n')

    return (solution, score)


def solve_revOrderFill(graph, num_buses, size_bus, constraints):

    solution = fillHelper(list(graph.nodes())[:: -1], num_buses)

    score = calcScore(graph.copy(), constraints, solution)
    print(str(score) + '\n')

    return (solution, score)


def fillHelper(lst, num_buses):
    solution = []
    buses = [[] for i in range(num_buses)]
    cap = int(len(lst) / num_buses)

    index = 0
    count = 0

    for n in lst:
        count += 1
        buses[index].append(n)
        if count >= cap:
            count = 0
            index += 1
        if index == num_buses:
            index = 0
            cap = 1
    for b in buses:
        solution.append(b)

    return solution




def calcScore(graph, constraints, sol):

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
    score = 0
    for edge in graph.edges():
        if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
            score += 1
    return score / total_edges

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''

    bestSoFar = load_dic()

    path = './all_inputs/' +  'small' + '/' + '1'
    graph, num_buses, size_bus, constraints = parse_input(path)

    for n in graph.nodes():
        graph.nodes[n]['friends'] = len(list(graph.adj[n]))

    lst = list(graph.nodes.data())
    lst.sort(key = lambda n : n[1]['friends'], reverse = True)

    print(lst)

    # for pair in graph.edges:
    #     graph[pair[0]][pair[1]]['value'] = graph.nodes[pair[0]]['friends'] + graph.nodes[pair[1]]['friends']
    #
    # for group in constraints:
    #     R = len(group)
    #     p = 2
    #     for i in range (R):
    #         for j in range (i + 1, R):
    #             if group[j] in list(graph.adj[group[i]]):
    #                 graph[group[i]][group[j]]['value'] *= (1 - 1 / ((R - 1) ** p))

    # print(graph.edges.data())

    # save_dic(bestSoFar)

    # graph, num_buses, size_bus, constraints = parse_input("testInputs/input1")
    # solution = solve(graph, num_buses, size_bus, constraints)
    # output_file = open("testOutputs/output1/output1.out", "w")
    #
    # for bus in solution:
    #     output_file.write(str(bus) + '\n')
    # output_file.close()

if __name__ == '__main__':
    main()
