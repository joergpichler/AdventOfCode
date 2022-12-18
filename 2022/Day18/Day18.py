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

def count_sides_pt2(map: set[tuple[int,int,int]]):
    min_x = min((x[0] for x in map))
    max_x = max((x[0] for x in map))
    min_y = min((x[1] for x in map))
    max_y = max((x[1] for x in map))
    min_z = min((x[2] for x in map))
    max_z = max((x[2] for x in map))

    count = 0 

    for coord in map:
        add = True
        for x in range(coord[0] - 1, min_x - 1, -1):
            next_x_neg = (x, coord[1], coord[2])
            if next_x_neg in map:
                add = False
                break
        if add:
            count += 1

        add = True
        for x in range(coord[0] + 1, max_x + 1, 1):
            next_x_pos = (x, coord[1], coord[2])
            if next_x_pos in map:
                add = False
                break
        if add:
            count += 1

        add = True
        for y in range(coord[1] - 1, min_y - 1, -1):
            next_y_neg = (coord[0], y, coord[2])
            if next_y_neg in map:
                add = False
                break
        if add:
            count += 1

        add = True
        for y in range(coord[1] + 1, max_y + 1, 1):
            next_y_pos = (coord[0], y, coord[2])
            if next_y_pos in map:
                add = False
                break
        if add:
            count += 1

        add = True
        for z in range(coord[2] - 1, min_z - 1, -1):
            next_z_neg = (coord[0], coord[1], z)
            if next_z_neg in map:
                add = False
                break
        if add:
            count += 1

        add = True
        for z in range(coord[2] + 1, max_z + 1, 1):
            next_z_pos = (coord[0], coord[1], z)
            if next_z_pos in map:
                add = False
                break
        if add:
            count += 1

    
    return count

def main():
    map = parse('test.txt')
    #assert count_sides(map) == 64
    assert count_sides_pt2(map) == 58

    map = parse('input.txt')
    print(f'{count_sides(map)}')
    print(f'{count_sides_pt2(map)}')

if __name__ == '__main__':
    main()
