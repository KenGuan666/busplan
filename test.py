import networkx as nx
import pickle
import random
import os

from utils.heap import MaxHeap, MinHeap
from clear import save_dic, load_dic

from solver import *

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

        # One rowdy dude that destroys the whole bus
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
    banning = True
    while heap.size() > 0:
        if index == num_buses:
            banned = [[] for i in range(num_buses)]
            banning = False
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
            if neighbor in banned[index] and banning:
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

    score = calcScore(originalGraph, constraints, solution)

    return (solution, score)

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
    directory = 'medium'
    subfolder = '234'
    
    path = path_to_inputs + '/' + directory + '/' + subfolder
    graph, num_buses, size_bus, constraints = parse_input(path)
    print(directory + ' ' + subfolder)

    solve = solve_basicFriends

    solution = solve(graph.copy(), num_buses, size_bus, constraints)

    if (solution[1] > bestSoFar[directory][subfolder]['score']):
        print('Improved ' + directory + ' ' + subfolder + ' by ' + str(solution[1] - bestSoFar[directory][subfolder]['score']))
        improved += 1

    print('improved: ' + str(improved))
    # graph, num_buses, size_bus, constraints = parse_input("testInputs/input1")
    # solution = solve(graph, num_buses, size_bus, constraints)
    # output_file = open("testOutputs/output1/output1.out", "w")
    #
    # for bus in solution:
    #     output_file.write(str(bus) + '\n')
    # output_file.close()

if __name__ == '__main__':
    main()
