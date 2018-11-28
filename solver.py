import networkx as nx
import pickle
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

    for n in graph.nodes():
        graph.nodes[n]['friends'] = len(list(graph.adj[n]))

    lst = list(graph.nodes.data())
    lst.sort(key = lambda n : n[1]['friends'], reverse = True)

    filled = []

    for bus in buses:
        curr = lst.pop()[0]
        if curr not in filled:
            filled.append(curr)
            bus.append(curr)
            for neighbor in list(graph.adj[curr]):
                if len(bus) < size_bus and neighbor[0] not in filled:
                    bus.append(neighbor[0])
                    filled.append(neighbor[0])

    if len(lst) > 0:
        for bus in buses:
            while len(bus) < size_bus and len(lst) > 0:
                next = lst.pop()[0]
                if next not in filled:
                    bus.append(next)
            if len(lst) == 0:
                break

    for b in buses:
        solution.append(b)

    score = calcScore(graph.copy(), constraints, solution)
    print(str(score) + '\n')

    return (solution, score)



def solve_naiveFriendsWithQueue(graph, num_buses, size_bus, constraints):

    return 0


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

    try:
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

    except:
        return 0

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

    for directory in ['small', 'medium', 'large']:
        subfolders = [x[1] for x in os.walk(path_to_inputs + '/' + directory)][0]
        for subfolder in subfolders:
            path = path_to_inputs + '/' + directory + '/' + subfolder
            graph, num_buses, size_bus, constraints = parse_input(path)
            print(directory + ' ' + subfolder)

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

            solution = solve(graph, num_buses, size_bus, constraints)

            if (solution[1] > bestSoFar[directory][subfolder]['score']):
                improved += 1
                total += solution[1]
                bestSoFar[directory][subfolder]['score'] = solution[1]
                bestSoFar[directory][subfolder]['method'] = method

                output_file = open(path_to_outputs + '/' + directory + '/' + subfolder + '.out', 'w+')
                for bus in solution[0]:
                    output_file.write(str(bus) + '\n')
                output_file.close()

            else:
                total += bestSoFar[directory][subfolder]['score']
                print('No improvement. Discarded.')

    print('total score: ' + str(total / 722))
    print('improved: ' + str(improved))
    bestSoFar['overall'] = total / 722

    save_dic(bestSoFar)

    # graph, num_buses, size_bus, constraints = parse_input("testInputs/input1")
    # solution = solve(graph, num_buses, size_bus, constraints)
    # output_file = open("testOutputs/output1/output1.out", "w")
    #
    # for bus in solution:
    #     output_file.write(str(bus) + '\n')
    # output_file.close()

if __name__ == '__main__':
    main()
