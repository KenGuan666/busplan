import pickle
import os

from clear import load_dic

bestSoFar = load_dic()

result = {'zeros': []}

for directory in ['small', 'medium', 'large']:
    subfolders = [x[1] for x in os.walk('./all_inputs/' + directory)][0]
    for subfolder in subfolders:
        if bestSoFar[directory][subfolder]['method'] not in result:
            result[bestSoFar[directory][subfolder]['method']] = 1
        else:
            result[bestSoFar[directory][subfolder]['method']] += 1
        if bestSoFar[directory][subfolder]['score'] == 0:
            result['zeros'].append(directory + '.' + subfolder)

result['score'] = bestSoFar['overall']

print(result)
