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


def modify_consecutive(solution, graph, num_buses, size_bus, constraints, prev_score):
    graph = graph.copy()
    edges = graph.number_of_edges()
    busScores = calc_LocalScore(graph, constraints, solution, size_bus)

    new_score = prev_score

    def swap():
        solution[i1][indexA], solution[i2][indexB] = solution[i2][indexB], solution[i1][indexA]

    improved = False
    rounds = 20
    while rounds > 0:
        i1, i2 = random.randint(0, len(solution) - 1), random.randint(0, len(solution) - 1)
        prev_local_score = busScores[i1] + busScores[i2]

        indexA, indexB = random.randint(0, len(solution[i1]) - 1), random.randint(0, len(solution[i2]) - 1)
        swap()

        local_score = calc_LocalScore(graph, constraints, [solution[i1], solution[i2]], size_bus)
        modified_score = sum(local_score)
        if modified_score > prev_local_score:
            improved = True
            new_score += (modified_score - prev_local_score) / edges
            busScores[i1], busScores[i2] = local_score[0], local_score[1]
            print('Improved by ', new_score - prev_score, ', ', rounds, ' rounds left.')
            rounds = min(rounds + 10, 100)
        else:
            swap()
            rounds -= 1

    if improved:
        return (solution, new_score - prev_score)
    return []

def modify_fillRandom(solution, graph, num_buses, size_bus, constraints, prev_score):
    graph = graph.copy()
    edges = graph.number_of_edges()

    busScores = calc_LocalScore(graph, constraints, solution, size_bus)
    valid_from = list(filter(lambda x: len(solution[x]) > 1, range(len(solution))))
    valid_to = list(filter(lambda x: len(solution[x]) < size_bus, range(len(solution))))
    if len(valid_from) == 0 or len(valid_to) == 0:
        return []
    if len(valid_from) == 1 and len(valid_to) == 1 and valid_from[0] == valid_to[0]:
        return []

    busF, busT = random.randint(0, len(valid_from) - 1), random.randint(0, len(valid_to) - 1)
    while valid_from[busF] == valid_to[busT]:
        busF, busT = random.randint(0, len(valid_from) - 1), random.randint(0, len(valid_to) - 1)
    busF, busT = valid_from[busF], valid_to[busT]
    prev_score = busScores[busF] + busScores[busT]

    def swap():
        solution[i1][indexA], solution[i2][indexB] = solution[i2][indexB], solution[i1][indexA]

    for _ in range(5):
        indexF = random.randint(0, len(solution[busF]) - 1)
        solution[busT].append(solution[busF].pop(indexF))
        modified_score = sum(calc_LocalScore(graph, constraints, [solution[busF], solution[busT]], size_bus))

        diff = modified_score - prev_score
        if diff > 0:
            return (solution, diff / edges)

        new_busScores = calc_LocalScore(graph, constraints, solution, size_bus)

        for _ in range(3):
            i1, i2 = random.randint(0, len(solution) - 1), random.randint(0, len(solution) - 1)
            prev_scoree = new_busScores[i1] + new_busScores[i2]

            for __ in range(3):
                indexA, indexB = random.randint(0, len(solution[i1]) - 1), random.randint(0, len(solution[i2]) - 1)
                swap()

                modified_scoree = sum(calc_LocalScore(graph, constraints, [solution[i1], solution[i2]], size_bus))
                if modified_scoree - prev_scoree + diff > 0:
                    return (solution, (modified_scoree - prev_scoree + diff) / edges)
                swap()

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
    if len(sys.argv) > 1:
        method = 'localImprove_' + sys.argv[1]

    num_iteration = 1
    if len(sys.argv) > 2:
        num_iteration = int(sys.argv[2])

    if method == 'localImprove_random':
        modify = modify_random
    elif method == 'localImprove_step':
        modify = modify_stepRandom
    elif method == 'localImprove_fill':
        modify = modify_fillRandom
    elif method == 'localImprove_consec':
        modify = modify_consecutive

    improved = {}

    for i in range(num_iteration):
        count = 0
        total = 0

        for size in ['medium']:
            subfolders = [x[1] for x in os.walk('all_inputs/' + size)][0]
            for number in subfolders:
                graph, num_buses, size_bus, constraints = parse_input(path_to_inputs + '/' + size + '/' + number)
                solution = parse_output(size, number)

                saved_score = dic[size][number]['score']

                modified = modify(solution, graph, num_buses, size_bus, constraints, saved_score)
                if len(modified) > 0:
                    if number in improved:
                        improved[number] += 1
                    else:
                        improved[number] = 1
                    modified_score = modified[1]
                    count += 1
                    print('improved ' + size + ' ' + number + ' by ' + str(modified_score))
                    dic[size][number]['score'] = modified_score + saved_score
                    dic[size][number]['improve_method'] = method
                    output_file = open(path_to_outputs + '/' + size + '/' + number + '.out', 'w+')
                    for bus in modified[0]:
                        output_file.write(str(bus) + '\n')
                    output_file.close()
                    save_dic(dic)
                else:
                    total += saved_score

        print('Improved: ' + str(count) + ' on ' + str(i) + 'th iteration.')
        print(improved)
        save_dic(dic)


if __name__ == '__main__':
    main()
