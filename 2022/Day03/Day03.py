def parse(file):
    with open(file, 'r') as f:
        return [l.strip() for l in f]

def get_item(l: str):
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

def main():
    data = parse('input.txt')
    sum = 0
    for d in data:
        item = get_item(d)
        value = get_value(item)
        sum += value
    print(sum)

if __name__ == '__main__':
    main()
