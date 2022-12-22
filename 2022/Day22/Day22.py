import re

class Map:
    def __init__(self, lines: list[str]) -> None:
        self.map = dict()
        self.ranges = dict()

        for line_idx in range(len(lines)):
            line = lines[line_idx]
            for char_idx in range(len(line)):
                char = line[char_idx]
                if char == ' ':
                    continue
                if not line_idx in self.ranges:
                    self.ranges[line_idx] = (char_idx, len(line) - 1)
                self.map[(char_idx, line_idx)] = char

def parse(file):

    def parse_instructions(line):
        instructions = []
        while len(line) > 0:
            number_match = re.match(r'^\d+', line)#
            if number_match:
                instructions.append(int(number_match.group()))
                line = line[number_match.span()[1]:]
            elif line[0] == 'R' or line[0] == 'L':
                instructions.append(line[0])
                line = line[1:]
            else:
                raise Exception
        return instructions

    map_lines = []
    with open(file, 'r') as f:
        line = f.readline().rstrip()
        while line != '':
            map_lines.append(line)
            line = f.readline().rstrip()
        instruction_line = f.readline().rstrip()

    return Map(map_lines), parse_instructions(instruction_line)

def play_pt1(map: Map, instructions: list):

    directions = ['r', 'd', 'l', 'u']

    def get_initial_position(map: Map):
        first_row_range = map.ranges[0]
        for i in range(first_row_range[0], first_row_range[1] + 1):
            if map.map[(i, 0)] == '.':
                break
        return (i, 0)

    def move(count, position, direction, map: Map):
        dx = 0
        dy = 0
        if direction == 'r':
            dx = 1
        elif direction == 'd':
            dy = 1
        elif direction == 'l':
            dx = -1
        elif direction == 'u':
            dy = -1
        
        for _ in range(count):
            next_position = (position[0] + dx, position[1] + dy)
            if next_position not in map.map:
                if direction == 'r':
                    next_position = (map.ranges[next_position[1]][0], next_position[1])
                elif direction == 'l':
                    next_position = (map.ranges[next_position[1]][1], next_position[1])
                elif direction == 'd':
                    for i in range(len(map.ranges)):
                        r = map.ranges[i]
                        if r[0] <= next_position[0] <= r[1]:
                            next_position = (next_position[0], i)
                            break
                    if next_position == position:
                        raise Exception
                elif direction == 'u':
                    for i in range(len(map.ranges) - 1, -1, -1):
                        r = map.ranges[i]
                        if r[0] <= next_position[0] <= r[1]:
                            next_position = (next_position[0], i)
                            break
                    if next_position == position:
                        raise Exception
            if next_position not in map.map:
                raise Exception
            tile = map.map[next_position]
            if tile == '.':
                position = next_position
            elif tile == '#':
                break
            else:
                raise Exception
                

        return position

    def turn(instruction, current_direction):
        direction_idx = directions.index(current_direction)
        if instruction == 'R':
            direction_idx = (direction_idx + 1) % len(directions)
        elif instruction == 'L':
            direction_idx -= 1
        else:
            raise Exception
        return directions[direction_idx]
    
    current_direction = 'r'
    current_position = get_initial_position(map)

    for instruction in instructions:
        if isinstance(instruction, int):
            current_position = move(instruction, current_position, current_direction, map)
        else:
            current_direction = turn(instruction, current_direction)
    
    return (1000 * (current_position[1] + 1)) + (4 * (current_position[0] + 1)) + directions.index(current_direction)

def main():
    map, instructions = parse('test.txt')
    assert play_pt1(map, instructions) == 6032

    map, instructions = parse('input.txt')
    print(f'{play_pt1(map, instructions)}') 

if __name__ == '__main__':
    main()
