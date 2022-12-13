class Pair:


    def __init__(self, l1, l2) -> None:
        self.l1 = self._parse(l1)
        self.l2 = self._parse(l2)


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


    def is_in_order(self):
        return self._is_in_order(self.l1, self.l2)

    def _is_in_order(self, e1, e2):
        result = None
        if isinstance(e1, int) and isinstance(e2, int):
            if e1 < e2:
                return True
            if e1 == e2:
                return None
            return False
        elif isinstance(e1, list) and isinstance(e2, list):
            for i in range(max(len(e1), len(e2))):
                elem1 = e1[i] if len(e1) > i else None
                elem2 = e2[i] if len(e2) > i else None
                if elem1 is None and elem2 is not None:
                    return True
                if elem1 is not None and elem2 is None:
                    return False
                result = self._is_in_order(elem1, elem2)
                if result is not None:
                    return result
        elif isinstance(e1, int) and isinstance(e2, list):
            result = self._is_in_order([e1], e2)
            if result is not None:
                return result
        elif isinstance(e1, list) and isinstance(e2, int):
            result = self._is_in_order(e1, [e2])
            if result is not None:
                return result
        else:
            raise Exception
        return result


def parse(file):
    packets = []
    with open(file, 'r') as f:
        while True:
            l1 = f.readline()
            l2 = f.readline()
            f.readline()
            if not l1 or not l2:
                break
            packets.append(Pair(l1.strip(), l2.strip()))
    return packets


def pt1(packets):
    ctr = 0
    sum = 0
    for p in packets:
        ctr += 1
        if p.is_in_order():
            sum += ctr
    return sum


def main():
    packets = parse('test.txt')
    assert pt1(packets) == 13
    
    packets = parse('input.txt')
    print(f'{pt1(packets)}')
    pass


if __name__ == '__main__':
    main()
