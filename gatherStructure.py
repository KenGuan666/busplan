import pickle
import os

from clear import load_dic

bestSoFar = load_dic()

result = {'zeros': [], 'perfects': 0}
result['bad smalls'] = []

for directory in ['small']:
    subfolders = [x[1] for x in os.walk('./all_inputs/' + directory)][0]
    for subfolder in subfolders:
        if bestSoFar[directory][subfolder]['method'] not in result:
            result[bestSoFar[directory][subfolder]['method']] = 1
        else:
            result[bestSoFar[directory][subfolder]['method']] += 1
        if bestSoFar[directory][subfolder]['score'] == 0:
            result['zeros'].append(directory + '.' + subfolder)
        if bestSoFar[directory][subfolder]['score'] == 1:
            result['perfects'] += 1
        # if bestSoFar[directory][subfolder]['score'] < 0.1:
        #     result['bad smalls'].append(directory + ' ' + subfolder + ': ' + str(bestSoFar[directory][subfolder]['score']))

result['score'] = bestSoFar['overall']

print(result)
