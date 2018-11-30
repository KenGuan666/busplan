import networkx as nx
import pickle
import random
import os
import sys

from clear import save_dic, load_dic
from solver import *

from correct import parse_output

def chance(n):
    return random.randint(0, n - 1) < n


def modify_fillRandom(solution, graph, num_buses, size_bus, constraints, prev_score):

    valid_from = list(filter(lambda x: len(solution[x]) > 1, range(len(solution))))
    valid_to = list(filter(lambda x: len(solution[x]) < size_bus, range(len(solution))))
    if len(valid_from) == 0 or len(valid_to) == 0:
        return []

    busF, busT = random.randint(0, len(valid_from) - 1), random.randint(0, len(valid_to) - 1)
    busF, busT = valid_from[busF], valid_to[busT]
    for _ in range(2):

        indexF= random.randint(0, len(solution[busF]) - 1)
        solution[busT].append(solution[busF].pop(indexF))

        randi = modify_stepRandom(solution, graph, num_buses, size_bus, constraints, prev_score)

        if len(randi) > 0:
            return randi

        solution[busF].append(solution[busT].pop(len(solution[busT]) - 1))

    return []

def modify_random(solution, graph, num_buses, size_bus, constraints, prev_score):
    graph = graph.copy()

    for _ in range(random.randint(1, 3)):
        for index in range(len(solution) - 1):
            if chance(80):
                indexA, indexB = random.randint(0, len(solution[index + 1]) - 1), random.randint(0, len(solution[index]) - 1)
                temp = solution[index + 1][indexA]
                solution[index + 1][indexA] = solution[index][indexB]
                solution[index][indexB] = temp

        modified_score = calcScore(graph, constraints, solution, size_bus)
        if modified_score > prev_score:
            return (solution, modified_score - prev_score)

    return []

def modify_stepRandom(solution, graph, num_buses, size_bus, constraints, prev):
    graph = graph.copy()
    busScores = calc_LocalScore(graph, constraints, solution, size_bus)

    def swap():
        solution[i1][indexA], solution[i2][indexB] = solution[i2][indexB], solution[i1][indexA]

    for _ in range(20):
        i1, i2 = random.randint(0, len(solution) - 1), random.randint(0, len(solution) - 1)
        prev_score = busScores[i1] + busScores[i2]

        for i in range(3):
            indexA, indexB = random.randint(0, len(solution[i1]) - 1), random.randint(0, len(solution[i2]) - 1)
            swap()

            modified_score = sum(calc_LocalScore(graph, constraints, [solution[i1], solution[i2]], size_bus))
            if modified_score > prev_score:
                return (solution, (modified_score - prev_score) / graph.number_of_edges())
            swap()

    return []

def main():

    count = 0
    dic = load_dic()

    method = 'localImprove_fill'
    num_modifications = 1

    if method == 'localImprove_random':
        modify = modify_random
    elif method == 'localImprove_step':
        modify = modify_stepRandom
    elif method == 'localImprove_fill':
        modify = modify_fillRandom

    for i in range(100):
        count = 0
        total = 0

        for size in ['small']:
            subfolders = [x[1] for x in os.walk('all_inputs/' + size)][0]
            for number in subfolders:
                graph, num_buses, size_bus, constraints = parse_input(path_to_inputs + '/' + size + '/' + number)
                solution = parse_output(size, number)

                saved_score = dic[size][number]['score']

                modified = modify(solution, graph, num_buses, size_bus, constraints, saved_score)
                if len(modified) > 0:
                    modified_score = modified[1]
                    count += 1
                    print('improved ' + size + ' ' + number + ' by ' + str(modified_score))
                    # dic[size][number]['score'] = modified_score + saved_score
                    # dic[size][number]['improve_method'] = method
                    # output_file = open(path_to_outputs + '/' + size + '/' + number + '.out', 'w+')
                    # for bus in modified[0]:
                    #     output_file.write(str(bus) + '\n')
                    # output_file.close()
                    save_dic(dic)
                else:
                    total += saved_score

        print('Improved: ' + str(count))
        save_dic(dic)


if __name__ == '__main__':
    main()
