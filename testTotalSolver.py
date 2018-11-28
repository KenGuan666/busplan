import networkx as nx
import random
import os

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
path_to_outputs = "."

num_rep = 1

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

def solve(graph, num_buses, size_bus, constraints):
    #TODO: Write this method as you like. We'd recommend changing the arguments here as well
    score = 0
    bestSol = []
    size = num_buses
    for _ in range(num_rep):
        size = num_buses
        solution = []
        buses = [[] for i in range(size)]
        for n in list(graph.nodes()):
            thisBus = random.randint(0, size - 1)
            buses[thisBus].append(n)
            if len(buses[thisBus]) == size_bus:
                solution.append(buses.pop(thisBus))
                size -= 1
        for b in buses:
            solution.append(b)

        curr_score = calcScore(graph.copy(), constraints, solution)
        print(str(curr_score) + '\n')
        if curr_score > score:
            score = curr_score
            bestSol = solution

    return bestSol

def calcScore(graph, constraints, sol):

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

    for directory in ['small', 'medium', 'large']:
        subfolders = [x[1] for x in os.walk(path_to_inputs + '/' + directory)][0]
        for subfolder in subfolders:
            path = path_to_inputs + '/' + directory + '/' + subfolder
            graph, num_buses, size_bus, constraints = parse_input(path)
            print(directory + ' ' + subfolder)
            solution = solve(graph, num_buses, size_bus, constraints)
            output_file = open(path_to_outputs + '/' + directory + '/' + subfolder + '.out', 'w+')
            for bus in solution:
                output_file.write(str(bus) + '\n')
            output_file.close()

    # graph, num_buses, size_bus, constraints = parse_input("testInputs/input1")
    # solution = solve(graph, num_buses, size_bus, constraints)
    # output_file = open("testOutputs/output1/output1.out", "w")
    #
    # for bus in solution:
    #     output_file.write(str(bus) + '\n')
    # output_file.close()


if __name__ == '__main__':
    main()
