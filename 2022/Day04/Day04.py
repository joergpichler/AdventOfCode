
class Range:

    def __init__(self, start, stop) -> None:
        self.start = start
        self.stop = stop

    def __repr__(self) -> str:
        return f'{self.start}-{self.stop}'

    def fully_contains(self, other):
        return other.start >= self.start and other.stop <= self.stop

    def overlaps(self, other):
        if other.start > self.stop or self.start > other.stop:
            return False
        return True


def parse(file):
    ranges = []
    with open(file, 'r') as f:
        for l in f:
            l = l.split(',')
            a = l[0].split('-')
            b = l[1].split('-')
            r1 = Range(int(a[0]), int(a[1]))
            r2 = Range(int(b[0]), int(b[1]))
            ranges.append((r1, r2))
    return ranges

def main():
    data = parse('input.txt')
    count = sum(map(lambda x: x[0].fully_contains(x[1]) or x[1].fully_contains(x[0]), data))
    print(count)
    count = sum(map(lambda x: x[0].overlaps(x[1]) or x[1].overlaps(x[0]), data))
    print(count)
    pass

if __name__ == '__main__':
    main()
