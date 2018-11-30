import networkx as nx
import pickle
import random
import os
from clear import save_dic, load_dic

from solver import *

def parse_output(size, number):
    buses = open('output_submission/busplan/' + size + '/' + number + ".out")
    results = []

    for line in buses:
        if line == "[]\n":
            return [[]]
        line = line[1: -2]
        curr_bus = [num.replace("'", "") for num in line.split(", ")]
        results.append(curr_bus)

    return results


def main():
    size = 'small'
    number = '11'

    count = 0
    dic = load_dic()

    for size in ['small']:
        subfolders = [x[1] for x in os.walk('all_inputs/' + size)][0]
        for number in subfolders:
            graph, num_buses, size_bus, constraints = parse_input(path_to_inputs + '/' + size + '/' + number)
            solution = parse_output(size, number)

            saved_score = dic[size][number]['score']

            actual_score = calcScore(graph, constraints, solution, size_bus)

            print('Looking at ' + size + ' ' + number)

            if not saved_score == actual_score:
                print(size + ' ' + number)
                print(saved_score - actual_score)
                dic[size][number]['score'] = actual_score
                count += 1
                save_dic(dic)

    print(count)
    # save_dic()


if __name__ == '__main__':
    main()
