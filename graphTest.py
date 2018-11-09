import networkx as nx
import random

G = nx.Graph()
# G = nx.read_gml('./testInputs/input1.gml')

def randomGraph(size, density):
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(size)])
    for i in range(size):
        for j in range(i + 1, size):
            if chance(density):
                graph.add_edge(i, j)
    return graph

def chance(num):
    return num >= random.randint(1, 100)

G = randomGraph(2000, 50)

nx.write_gml(G, './testInputs/input1/graph.gml')
