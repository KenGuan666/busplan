import networkx as nx
import pickle
import random
import os
import sys

from clear import save_dic, load_dic
from solver import *
from localImprove import *

from correct import parse_output

def main():

    count = 0
    dic = load_dic()

    method = 'localImprove_fill'
    if len(sys.argv) > 3:
        method = 'localImprove_' + sys.argv[3]

    num_iteration = 10
    if len(sys.argv) > 4:
        num_iteration = int(sys.argv[4])

    if method == 'localImprove_random':
        modify = modify_random
    elif method == 'localImprove_step':
        modify = modify_stepRandom
    elif method == 'localImprove_fill':
        modify = modify_fillRandom
    elif method == 'localImprove_consec':
        modify = modify_consecutive

    size = sys.argv[1]
    number = sys.argv[2]

    count = 0

    for i in range(num_iteration):
        total = 0

        graph, num_buses, size_bus, constraints = parse_input(path_to_inputs + '/' + size + '/' + number)
        solution = parse_output(size, number)

        saved_score = dic[size][number]['score']

        modified = modify(solution, graph, num_buses, size_bus, constraints, saved_score)
        if len(modified) > 0:
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

        save_dic(dic)

    print('Improved: ' + str(count))


if __name__ == '__main__':
    main()
