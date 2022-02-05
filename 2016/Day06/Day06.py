from collections import defaultdict
import numpy as np

def parse(file):
    lines = []
    with open(file, 'r') as f:
        for line in f:
            lines.append([c for c in line.strip()])
    return np.array(lines)

def get_string(data, pt2 = False):
    result = ''
    for i in range(data.shape[1]):
        characters = data[:,i]
        column_dict = defaultdict(int)
        for character in characters:
            column_dict[character] += 1
        character = sorted(column_dict.items(), key=lambda x: -x[1])[-1 if pt2 else 0][0]
        result += character
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
