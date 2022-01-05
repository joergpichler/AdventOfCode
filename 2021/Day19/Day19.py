import re

import numpy as np
import re

class Scanner:
    def __init__(self, number):
        self.number = number
        self.beacons = []
        pass

    def add_coords(self, coords):
        self.beacons.append(np.array(coords))

    def __repr__(self) -> str:
        return 'Scanner ' + str(self.number)

    def contains_vector(self, vector) -> bool:
        for i in range(len(self.beacons)):
            b1 = self.beacons[i]
            for j in range(len(self.beacons)):
                if i == j:
                    continue
                b2 = self.beacons[j]
                vec = b2 - b1
                cross = np.cross(vec, vector)
                if np.count_nonzero(cross) == 0: # and np.linalg.norm(vec) == np.linalg.norm(vector):
                    return True
        return False

    def get_vectors(self):
        for i in range(len(self.beacons)):
            b1 = self.beacons[i]
            for j in range(len(self.beacons)):
                if i == j:
                    continue
                b2 = self.beacons[j]
                yield b2 - b1


def parse(file):
    scanners = []
    scanner = None
    with open(file, 'r') as f:
        for line in f:
            match = re.match(r"--- scanner (\d+) ---", line)
            if match:
                if scanner is not None:
                    scanners.append(scanner)
                scanner = Scanner(int(match.group(1)))
                continue
            elif line and line.strip():
                coords = list(map(int, line.strip().split(',')))
                scanner.add_coords(coords)
            else:
                continue
    scanners.append(scanner)
    return scanners


def main():
    scanners = parse('demo.txt')
    count = 0
    for vector in scanners[1].get_vectors():
        if scanners[0].contains_vector(vector):
            count += 1

    print(count)


if __name__ == '__main__':
    pass
    main()
