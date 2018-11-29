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

def modify_random(solution, graph, num_buses, size_bus, constraints):
    for i in range(random.randint(1, 5)):
        for index in range(len(solution) - 1):
            if chance(80):
                indexA, indexB = random.randint(0, len(solution[index + 1]) - 1), random.randint(0, len(solution[index]) - 1)
                temp = solution[index + 1][indexA]
                solution[index + 1][indexA] = solution[index][indexB]
                solution[index][indexB] = temp

    return solution

def modify_busScore(solution, grpah, num_buses, size_bus, constraints):

    return solution

def main():

    count = 0
    dic = load_dic()

    method = 'localImprove_random'
    num_modifications = 1

    if method == 'localImprove_random':
        modify = modify_random

    count = 0
    total = 0

    for _ in range(100):
        for size in ['small', 'medium', 'large']:
            subfolders = [x[1] for x in os.walk('all_inputs/' + size)][0]
            for number in subfolders:
                graph, num_buses, size_bus, constraints = parse_input(path_to_inputs + '/' + size + '/' + number)
                solution = parse_output(size, number)

                saved_score = dic[size][number]['score']

                for i in range (num_modifications):
                    modified = modify(solution, graph, num_buses, size_bus, constraints)
                    modified_score = calcScore(graph, constraints, modified)
                    if modified_score > saved_score:
                        total += modified_score
                        count += 1
                        print('improved ' + size + ' ' + number + ' by ' + str(modified_score - saved_score))
                        dic[size][number]['score'] = modified_score
                        dic[size][number]['improve_method'] = method
                        output_file = open(path_to_outputs + '/' + size + '/' + number + '.out', 'w+')
                        for bus in solution:
                            output_file.write(str(bus) + '\n')
                        output_file.close()
                        save_dic(dic)
                    else:
                        total += saved_score

        print('Improved: ' + str(count))
        print(total / 722)
        dic['overall'] = total / 722
        save_dic(dic)


if __name__ == '__main__':
    main()
