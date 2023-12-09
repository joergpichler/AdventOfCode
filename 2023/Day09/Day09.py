import regex as re

def parse(file):
    result = []
    with open(file, 'r') as f:
        for l in f:
            result.append([int(x) for x in re.findall(r'-?\d+', l)])
    return result    

def diff_row(row):
    data = [row]
    while not all(x == 0 for x in data[-1]):
        row = data[-1]
        next_row = []
        for i in range(1, len(row)):
            next_row.append(row[i] - row[i - 1])
        data.append(next_row)
    return data

def find_num_right(row):
    data = diff_row(row)
    data[-1].append(0)
    for i in range(len(data) - 2, -1, -1):
        data[i].append(data[i][-1] + data[i + 1][-1])
    return data[0][-1]

def find_num_left(row):
    data = diff_row(row)
    data[-1].insert(0, 0)
    for i in range(len(data) - 2, -1, -1):
        data[i].insert(0, data[i][0] - data[i + 1][0])
    return data[0][0]


def pt1(data):
    return sum((find_num_right(x) for x in data))

def pt2(data):
    return sum((find_num_left(x) for x in data))

def main():
    data = parse('test.txt')
    assert pt1(data) == 114
    assert pt2(data) == 2

    data = parse('input.txt')
    print(pt1(data))
    print(pt2(data))

if __name__ == '__main__':
    main()
