import pickle

def save_dic(obj):
    with open('dic.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_dic():
    with open('dic.pkl', 'rb') as f:
        return pickle.load(f)

raw = []

dic = load_dic()

for s in raw:
    lst = s.split('_')
    dic[lst[0]][lst[1]]['score'] = 0
    dic[lst[0]][lst[1]]['method'] = 'None'

# for directory in ['small', 'medium', 'large']:
#     subfolders = [x[1] for x in os.walk('all_inputs/' + directory)][0]
#     for subfolder in subfolders:
#         if dic[directory][subfolder]['method'] == 'localImprove_random':
#             dic[directory][subfolder]['score'] = 0
#             dic[directory][subfolder]['method'] = 'None'


save_dic(dic)
