import pickle

def load_dic():
    with open('dic.pkl', 'rb') as f:
        return pickle.load(f)

dic = load_dic()

size = 'small'
number = '1'

print(dic[size][number]['score'])
print(dic[size][number]['method'])
