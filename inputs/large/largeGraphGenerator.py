import networkx as nx
import random


G = nx.Graph()
# G = nx.read_gml('./testInputs/input1.gml')

def graphGenerator(size):
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(1, size+1)])  #add nodes 1 to 49
    rowdyStart = int((size+1)/2 + 1) #26

    for i in range(2, rowdyStart):   # from 2 to 25, add friend 1
        graph.add_edge(1, i)

    for j in range(rowdyStart, size+1):  #from 26 to 49, we choose 5 random student from 2 to 25, add edge.
        for k in range(50):
            num = random.randint(2, rowdyStart - 1)
            graph.add_edge(j, num)


    parameters_file = open("./inputs/large/parameters.txt", "w")
    parameters_file.write(str(2) + '\n')
    parameters_file.write(str(size) + '\n')
    #the following defines the rowdy groups, whcih are the pairs (1, k), k from 26 to 49
    for i in range (rowdyStart, size+1):
        parameters_file.write(str([1, i]) + '\n')

    parameters_file.close()


    return graph

G = graphGenerator(999)

nx.write_gml(G, './inputs/large/graph.gml')
