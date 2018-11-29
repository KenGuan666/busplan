import pickle
import sys

from clear import load_dic

dic = load_dic()

size = sys.argv[1]
number = sys.argv[2]

print(dic[size][number]['score'])
print(dic[size][number]['method'])
if 'improve_method' in dic[size][number]:
    print(dic[size][number]['improve_method'])
