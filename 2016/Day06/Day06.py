from collections import defaultdict
import numpy as np

def parse(file):
    arr = []
    with open(file, 'r') as f:
        for l in f:
            arr.append([x for x in l.strip()])
    return np.array(arr)

def get_string(data, pt2 = False):
    result = ''
    for i in range(data.shape[1]):
        col = data[:,i]
        d = defaultdict(int)
        for c in col:
            d[c] += 1
        c = sorted(d.items(), key=lambda x: -x[1])[-1 if pt2 else 0][0]
        result += c
    return result

def main():
    data = parse('test.txt')
    assert get_string(data) == 'easter'
    assert get_string(data, True) == 'advent'

    data = parse('input.txt')
    print(f'Pt1: {get_string(data)}')
    print(f'Pt2: {get_string(data, True)}')

if __name__ == '__main__':
    main()
