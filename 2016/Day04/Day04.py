from collections import defaultdict

class Room:
    def __init__(self, str) -> None:
        import re
        match = re.match(r'^(.+?)-(\d+)(?:\[(.+)\])?$', str)
        self.name = match.group(1)
        self.sector_id = int(match.group(2))
        self.checksum = match.group(3)

    def _calc_checksum(self):
        d = defaultdict(int)
        for c in self.name:
            if c == '-':
                continue
            d[c] += 1
        s = list(sorted(d.items(), key=lambda x: (-x[1], x[0])))
        assert len(s) >= 5
        checksum = ''
        for i in range(5):
            checksum += s[i][0]
        return checksum

    @property
    def is_real(self):
        return self.checksum == self._calc_checksum()

    def __repr__(self) -> str:
        return f'{self.is_real}: {self.name}-{self.sector_id}[{self.checksum}]'

    def decrypt(self):
        result = ''
        for c in self.name:
            if c == '-':
                result += ' '
            else:
                code = ord(c) - ord('a')
                code += self.sector_id
                code = code % (ord('z') - ord('a') + 1)
                result += chr(code + ord('a'))
        return result

def parse(file):
    with open(file, 'r') as f:
        return [Room(l.strip()) for l in f]

def main():
    rooms = parse('test.txt')
    sector_id_sum = sum((r.sector_id for r in rooms if r.is_real))
    assert sector_id_sum == 1514

    rooms = parse('input.txt')
    sector_id_sum = sum((r.sector_id for r in rooms if r.is_real))
    print(f'Pt1: {sector_id_sum}')

    assert Room('qzmt-zixmtkozy-ivhz-343').decrypt() == 'very encrypted name'

    sector_id = -1
    for r in (r for r in rooms if r.is_real):
        if "north" in r.decrypt():
            print(r.decrypt())
            sector_id = r.sector_id
            break
    print(f'Pt2: {sector_id}')

if __name__ == '__main__':
    main()
