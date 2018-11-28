import networkx as nx
import pickle
import random
import os

def save_dic(obj):
    with open('dic.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_dic():
    with open('dic.pkl', 'rb') as f:
        return pickle.load(f)

def parse_input(size, number):
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
    graph = nx.read_gml('all_inputs/' + size + '/' + number + "/graph.gml")
    parameters = open('all_inputs/' + size + '/' + number + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

def parse_output(size, number):
    buses = open('output_submission/busplan/' + size + '/' + number + ".out")
    results = []

    for line in buses:
        if line == "[]\n":
            return [[]]
        line = line[1: -2]
        curr_bus = [num.replace("'", "") for num in line.split(", ")]
        results.append(curr_bus)

    return results

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
    size = 'small'
    number = '11'

    count = 0
    dic = load_dic()

    for size in ['small', 'medium', 'large']:
        subfolders = [x[1] for x in os.walk('all_inputs/' + size)][0]
        for number in subfolders:
            graph, num_buses, size_bus, constraints = parse_input(size, number)
            solution = parse_output(size, number)

            saved_score = dic[size][number]['score']

            actual_score = calcScore(graph, constraints, solution)

            if saved_score > actual_score:
                print(size + ' ' + number)
                count += 1

    print(count)
    # save_dic()


if __name__ == '__main__':
    main()
