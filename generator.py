import networkx as nx
import random

G = nx.Graph()
sizes = [['small', 50], ['medium', 500], ['large', 1000]]
# G = nx.read_gml('./testInputs/input1.gml')

def graphGenerator(size):
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(1, size)])  #add nodes 1 to 49
    rowdyStart = int((size)/2 + 1) #26

    for i in range(2, rowdyStart):   # from 2 to 25, add friend 1
        graph.add_edge(1, i)

    for j in range(rowdyStart, size):  #from 26 to 49, we choose 5 random student from 2 to 25, add edge.
        for k in range(5):
            num = random.randint(2, rowdyStart - 1)
            graph.add_edge(j, num)


    parameters_file = open("./inputs/small/parameters.txt", "w")
    parameters_file.write(str(2) + '\n')
    parameters_file.write(str(size - 1) + '\n')
    #the following defines the rowdy groups, whcih are the pairs (1, k), k from 26 to 49
    for i in range (rowdyStart, size):
        parameters_file.write(str([1, i]) + '\n')

    parameters_file.close()
    return graph

def generateOutput(name, size):
    output_file = open("./outputs/" + name + ".out", "w")
    output_file.write("[1]" + '\n')

    groupStr = str([i for i in range (2, size)])
    output_file.write(groupStr + '\n')
    output_file.close()

for options in sizes:
    G = graphGenerator(options[1])
    nx.write_gml(G, './inputs/' + options[0] + '/graph.gml')
    generateOutput(options[0], options[1])
