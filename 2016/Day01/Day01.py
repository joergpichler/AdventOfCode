def parse(file):
    with open(file, 'r') as f:
        return f.readline()

def _parse_instructions(s: str):
    return [x.strip() for x in s.split(',')]

def _get_diff(c1, c2):
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]
    len = max(abs(dx), abs(dy))
    for i in range(1, len + 1):
        yield (int(c1[0] + (dx / len) * i), int(c1[1] + (dy / len) * i))

def get_blocks(input: str, pt2: bool = False):
    instructions = _parse_instructions(input)

    orientation = 0 # 0: north, 1: east, 2: south, 3: west
    coords = [0, 0]

    if pt2:
        visited = set()
        visited.add(tuple(coords))

    for instruction in instructions:
        turn = instruction[:1]
        distance = int(instruction[1:])

        if turn == 'R':
            orientation = (orientation + 1) % 4
        else:
            orientation -= 1
            if orientation == -1:
                orientation = 3

        if pt2:
            old_coords = tuple(coords)

        if orientation == 0:
            coords[0] -= distance
        elif orientation == 1:
            coords[1] += distance
        elif orientation == 2:
            coords[0] += distance
        elif orientation == 3:
            coords[1] -= distance

        if pt2:
            new_coords = tuple(coords)
            for coord in _get_diff(old_coords, new_coords):
                if coord in visited:
                    return abs(coord[0]) + abs(coord[1])
                else:
                    visited.add(coord)
                
    return abs(coords[0]) + abs(coords[1])

def test():
    assert get_blocks('R2, L3') == 5
    assert get_blocks('R2, R2, R2') == 2
    assert get_blocks('R5, L5, R5, R3') == 12

    assert get_blocks('R8, R4, R4, R8', True) == 4

def main():
    test()
    instructions = parse('input.txt')
    print(f'Pt1: {get_blocks(instructions)}')
    print(f'Pt2: {get_blocks(instructions, True)}')

if __name__ == '__main__':
    main()
