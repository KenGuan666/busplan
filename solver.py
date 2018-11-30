import networkx as nx
import pickle
import random
import os
import sys

from clear import save_dic, load_dic
from utils.heap import MaxHeap, MinHeap

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

    for n in graph.nodes():
        graph.nodes[n]['friends'] = len(list(graph.adj[n]))

    nodes = list(graph.nodes())

    lst = list(graph.nodes.data())
    lst.sort(key = lambda n : n[1]['friends'], reverse = True)

    lst = [x[0] for x in lst]

    filled = []

    for bus in buses:
        curr = lst.pop()
        if curr not in filled:
            filled.append(curr)
            bus.append(curr)
            for neighbor in list(graph.adj[curr]):
                if len(bus) < size_bus and neighbor in nodes and neighbor not in filled:
                    bus.append(neighbor)
                    filled.append(neighbor)

    if len(lst) > 0:
        for bus in buses:
            while len(bus) < size_bus and len(lst) > 0:
                next = lst.pop()
                if next not in filled:
                    bus.append(next)
            if len(lst) == 0:
                break

    for b in buses:
        solution.append(b)

    score = calcScore(graph.copy(), constraints, solution, size_bus)

    return (solution, score)


def solve_basicFriends(graph, num_buses, size_bus, constraints):

    originalGraph = graph.copy()

    threshold = 0.05

    solution = []
    buses = [[] for i in range(num_buses)]

    for n in graph.nodes():
        graph.nodes[n]['friends'] = len(list(graph.adj[n]))
        graph.nodes[n]['edgeVal'] = float('inf')

    nodes = list(graph.nodes())

    toRemove = []
    for pair in graph.edges:
        if pair[0] == pair[1]:
            toRemove.append(pair[0])
            continue
        graph[pair[0]][pair[1]]['value'] = max(graph.nodes[pair[0]]['friends'], graph.nodes[pair[1]]['friends'])
        graph[pair[0]][pair[1]]['rowdy'] = 1

    for node in toRemove:
        graph.remove_edge(node, node)

    for group in constraints:
        R = len(group)
        p = 2

        if R > size_bus or R > 80:
            continue

        # One rowdy dude that is destined to go home
        if R == 1:
            for neighbor in graph.adj[group[0]]:
                graph[neighbor][group[0]]['rowdy'] = 0
        else:
            for i in range (R):
                for j in range (i + 1, R):
                    if group[j] in list(graph.adj[group[i]]):
                        graph[group[i]][group[j]]['rowdy'] *= (1 - 1 / ((R - 1) ** p))

    heap = MaxHeap(list(graph.nodes()), lambda x: len(graph.adj[x]))

    index = 0
    banned = [[] for i in range(num_buses)]
    while heap.size() > 0:
        if index == num_buses:
            banned = [[] for i in range(num_buses)]
            index = 0
            continue

        if len(buses[index]) == size_bus:
            index += 1
            continue

        lead = heap.pop()

        buses[index].append(lead)

        neighbors = list(graph.adj[lead])

        for n in neighbors:
            if graph[lead][n]['rowdy'] < threshold:
                banned[index].append(n)
            graph.nodes[n]['edgeVal'] = min(graph.nodes[n]['edgeVal'], graph[n][lead]['value'])
            graph.remove_edge(lead, n)

        friendHeap = MinHeap(neighbors, lambda x: graph.nodes[x]['edgeVal'])
        while len(buses[index]) < size_bus and friendHeap.size() > 0:
            neighbor = friendHeap.pop()
            if neighbor in banned[index]:
                continue
            heap.remove(neighbor)
            buses[index].append(neighbor)

            neighborbors = list(graph.adj[neighbor])

            for n in neighborbors:
                graph.nodes[n]['edgeVal'] = min(graph.nodes[n]['edgeVal'], graph[n][neighbor]['value'])
                graph.remove_edge(neighbor, n)

            friendHeap.insert(list(graph.adj[neighbor]))

        index += 1

    for b in buses:
        solution.append(b)

    score = calcScore(originalGraph, constraints, solution, size_bus)

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

    score = calcScore(graph.copy(), constraints, solution, size_bus)

    return (solution, score)


def solve_random(graph, num_buses, size_bus, constraints):

    lst = list(graph.nodes())
    random.shuffle(lst)
    solution = fillHelper(lst, num_buses)

    score = calcScore(graph.copy(), constraints, solution, size_bus)

    return (solution, score)


def solve_fastOrderFill(graph, num_buses, size_bus, constraints):

    solution = fillHelper(list(graph.nodes()), num_buses)

    score = calcScore(graph.copy(), constraints, solution, size_bus)

    return (solution, score)


def solve_revOrderFill(graph, num_buses, size_bus, constraints):

    solution = fillHelper(list(graph.nodes())[:: -1], num_buses)

    score = calcScore(graph.copy(), constraints, solution, size_bus)

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


def calc_LocalScore(graph, constraints, sol, size_bus):
    graph = graph.copy()

    for bus in sol:
        if len(bus) == 0:
            return [0]

    bus_assignments = {}
    attendance_count = 0

    # make sure each student is in exactly one bus
    attendance = {student:False for student in graph.nodes()}
    for i in range(len(sol)):
        for student in sol[i]:
            attendance[student] = True
            bus_assignments[student] = i

    # Remove nodes for rowdy groups which were not broken up
    for i in range(len(constraints)):
        if len(constraints[i]) > size_bus:
            continue
        busses = set()
        keep = True
        for student in constraints[i]:
            if student not in bus_assignments:
                keep = False
                break
            busses.add(bus_assignments[student])
        if keep and len(busses) <= 1:
            for student in constraints[i]:
                if student in graph:
                    graph.remove_node(student)

    # score output
    score = [graph.subgraph(bus).number_of_edges() for bus in sol]
    # score = [0] * len(sol)
    # for edge in graph.edges():
    #     if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
    #         score[bus_assignments[edge[0]]] += 1
    return score


def calcScore(graph, constraints, sol, size_bus):
    for bus in sol:
        if len(bus) > size_bus or len(bus) <= 0:
            return 0

    bus_assignments = {}

    # make sure each student is in exactly one bus
    attendance = {student:False for student in graph.nodes()}
    for i in range(len(sol)):
        for student in sol[i]:
            # if a student appears more than once

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
    score = score / total_edges

    return score


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

    method = 'naiveFriends'
    if len(sys.argv) > 1:
        method = sys.argv[1]

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

    for directory in ['small', 'medium', 'large']:
        subfolders = [x[1] for x in os.walk(path_to_inputs + '/' + directory)][0]
        for subfolder in subfolders:

            if method == 'None':
                total += bestSoFar[directory][subfolder]['score']
                continue

            path = path_to_inputs + '/' + directory + '/' + subfolder
            graph, num_buses, size_bus, constraints = parse_input(path)

            if method in ['fastOrderFill', 'fastOrder', 'revOrderFill', 'naiveFriends', 'basicFriends']:
                if bestSoFar[directory][subfolder]['method'] == method:
                    print('Same deterministic result. Skipped.')
                    total += bestSoFar[directory][subfolder]['score']
                    continue

            solution = solve(graph.copy(), num_buses, size_bus, constraints)

            if (solution[1] > bestSoFar[directory][subfolder]['score']):
                print('Improved ' + directory + ' ' + subfolder + ' by ' + str(solution[1] - bestSoFar[directory][subfolder]['score']))
                improved += 1
                total += solution[1]
                bestSoFar[directory][subfolder]['score'] = solution[1]
                bestSoFar[directory][subfolder]['method'] = method

                output_file = open(path_to_outputs + '/' + directory + '/' + subfolder + '.out', 'w+')
                for bus in solution[0]:
                    output_file.write(str(bus) + '\n')
                output_file.close()
                save_dic(bestSoFar)

            else:
                total += bestSoFar[directory][subfolder]['score']

    print('total score: ' + str(total / 722))
    print('improved: ' + str(improved))
    bestSoFar['overall'] = total / 722

    save_dic(bestSoFar)


if __name__ == '__main__':
    main()
