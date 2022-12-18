import re

def parse(file):
    map = set()
    with open(file, 'r') as f:
        for l in f:
            match = re.match(r'(\d+),(\d+),(\d+)', l)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                z = int(match.group(3))
                map.add((x,y,z))
    return map

def count_sides(map: set[tuple[int,int,int]]):
    count = 0
    for coord in map:
        for side in range(3):
            next_minus = (coord[0] - 1 if side == 0 else coord[0], coord[1] - 1 if side == 1 else coord[1], coord[2] - 1 if side == 2 else coord[2])
            next_plus = (coord[0] + 1 if side == 0 else coord[0], coord[1] + 1 if side == 1 else coord[1], coord[2] + 1 if side == 2 else coord[2])
            if next_minus not in map:
                count += 1
            if next_plus not in map:
                count +=1
    return count

def main():
    map = parse('test.txt')
    assert count_sides(map) == 64

    map = parse('input.txt')
    print(f'{count_sides(map)}')

if __name__ == '__main__':
    main()
