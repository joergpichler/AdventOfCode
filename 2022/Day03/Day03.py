def parse(file):
    with open(file, 'r') as f:
        return [l.strip() for l in f]

def get_item_1(l: str):
    if len(l) % 2 != 0:
        raise Exception
    a = list(l[:len(l)//2])
    b = list(l[len(l)//2:])
    return set(a).intersection(b).pop()

def get_value(item: str):
    if item.isupper():
        val = ord(item) - ord('A') + 27
    else:
        val = ord(item) - ord('a') + 1
    return val

def get_item_2(data: list[str]):
    if len(data) != 3:
        raise Exception
    r = (set(data[0]) & set(data[1]) & set(data[2])).pop()
    return r

def get_results(file):
    data = parse(file)
    sum = 0
    for d in data:
        item = get_item_1(d)
        value = get_value(item)
        sum += value
    sum2 = 0
    for i in range(0, len(data), 3):
        d = data[i:i+3]
        item = get_item_2(d)
        value = get_value(item)
        sum2 += value
    return (sum, sum2)

def main():
    
    results = get_results('test.txt')
    assert results[0] == 157
    assert results[1] == 70

    results = get_results('input.txt')
    print(f'Pt1: {results[0]}')
    print(f'Pt2: {results[1]}')

if __name__ == '__main__':
    main()
