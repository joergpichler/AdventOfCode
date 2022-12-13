from functools import cmp_to_key

class Packet:


    def __init__(self, l) -> None:
        self.l = self._parse(l)


    def _parse(self, l):
        lists = [[]]

        token = ''
        for i in range(0, len(l)):
            c = l[i]
            if i == 0:
                if c != '[':
                    raise Exception
                continue
            elif i == len(l) -1:
                if c != ']':
                    raise Exception
                if token != '':
                    lists[-1].append(self._parse_token(token))
                    token = ''
            elif c == ',':
                if token != '':
                    lists[-1].append(self._parse_token(token))
                    token = ''
            elif c == '[':
                new_list = []
                lists[-1].append(new_list)
                lists.append(new_list)
            elif c == ']':
                if token != '':
                    lists[-1].append(self._parse_token(token))
                    token = ''
                lists.pop(len(lists) - 1)
            else:
                token += l[i]

        return lists[0]


    def _parse_token(self, token):
        return int(token)


def parse(file):
    cache = []
    with open(file, 'r') as f:
        for l in f:
            l = l.strip()
            if l != '':
                cache.append(l)
    return [Packet(c) for c in cache]


def compare(e1, e2):
    result = 0
    if isinstance(e1, Packet) and isinstance(e2, Packet):
        return compare(e1.l, e2.l)
    if isinstance(e1, int) and isinstance(e2, int):
        if e1 < e2:
            return -1
        if e1 == e2:
            return 0
        return 1
    elif isinstance(e1, list) and isinstance(e2, list):
        for i in range(max(len(e1), len(e2))):
            elem1 = e1[i] if len(e1) > i else None
            elem2 = e2[i] if len(e2) > i else None
            if elem1 is None and elem2 is not None:
                return -1
            if elem1 is not None and elem2 is None:
                return 1
            result = compare(elem1, elem2)
            if result != 0:
                return result
    elif isinstance(e1, int) and isinstance(e2, list):
        result = compare([e1], e2)
        if result != 0:
            return result
    elif isinstance(e1, list) and isinstance(e2, int):
        result = compare(e1, [e2])
        if result != 0:
            return result
    else:
        raise Exception
    return result

def pt1(packets):
    ctr = 0
    sum = 0
    for i in range(0, len(packets), 2):
        ctr += 1
        p1 = packets[i]
        p2 = packets[i + 1]
        result = compare(p1, p2)
        if result < 0:
            sum += ctr
    return sum

def pt2(packets):
    tmp = list(packets)
    p1 = Packet('[[2]]')
    p2 = Packet('[[6]]')
    tmp.append(p1)
    tmp.append(p2)

    tmp = sorted(tmp, key=cmp_to_key(compare))

    return (tmp.index(p1) + 1) * (tmp.index(p2) + 1)

def main():
    packets = parse('test.txt')
    assert pt1(packets) == 13
    assert pt2(packets) == 140
    
    packets = parse('input.txt')
    print(f'{pt1(packets)}')
    print(f'{pt2(packets)}')
    pass


if __name__ == '__main__':
    main()
