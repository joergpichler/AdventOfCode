from collections import defaultdict
import sys

class Elf:
    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position

    def __repr__(self) -> str:
        return f'{self.position}'

class ElfMap:
    def __init__(self, elves: list[Elf]) -> None:
        self.map = set(map(lambda x: x.position, elves))

    def has_adjacent_elf(self, elf: Elf):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == dy == 0:
                    continue
                pos = (elf.position[0] + dx, elf.position[1] + dy)
                if pos in self.map:
                    return True
        return False

    def _get_min_max(self):
        min_x = sys.maxsize
        max_x = -sys.maxsize - 1
        min_y = sys.maxsize
        max_y = -sys.maxsize - 1
        for pos in self.map:
            min_x = min(min_x, pos[0])
            max_x = max(max_x, pos[0])
            min_y = min(min_y, pos[1])
            max_y = max(max_y, pos[1])
        return min_x, max_x, min_y, max_y

    def get_empty_tiles(self):
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for pos in self.map:
            min_x = min(min_x, pos[0])
            max_x = max(max_x, pos[0])
            min_y = min(min_y, pos[1])
            max_y = max(max_y, pos[1])
        dx = max_x - min_x
        dy = max_y - min_y
        return ((dx + 1) * (dy + 1)) - len(self.map)

    def move(self, elf: Elf, new_pos: tuple[int, int]):
        self.map.remove(elf.position)
        elf.position = new_pos
        self.map.add(elf.position)
        pass

    def debug_print(self):
        min_x, max_x, min_y, max_y = self._get_min_max()
        for row in range(min_y, max_y + 1):
            line = ''
            for col in range(min_x, max_x + 1):
                line += '#' if (col, row) in self.map else '.'
            print(line)
        print()


def calc_move(elf: Elf, elf_map: ElfMap, directions: list[str]):
    
    for d in directions:
        d_x = 0
        d_y = 0

        if d == 'n':
            d_y = -1
        elif d == 's':
            d_y = 1
        elif d == 'w':
            d_x = -1
        elif d == 'e':
            d_x = 1
        else:
            raise Exception

        has_elf_in_direction = False
        
        if d_x == 0:
            proposed_move = (elf.position[0], elf.position[1] + d_y)
            for dx in range(-1, 2):
                pos = (elf.position[0] + dx, elf.position[1] + d_y)
                if pos in elf_map.map:
                    has_elf_in_direction = True 
                    break
        if d_y == 0:
            proposed_move = (elf.position[0] + d_x, elf.position[1])
            for dy in range(-1, 2):
                pos = (elf.position[0] + d_x, elf.position[1] + dy)
                if pos in elf_map.map:
                    has_elf_in_direction = True 
                    break

        if not has_elf_in_direction:
            return proposed_move

    return elf.position

def parse(file):
    elves = []
    row = 0
    with open(file, 'r') as f:
        for l in f:
            l = list(l.strip())
            for i in range(len(l)):
                c = l[i]
                if c == '#':
                    elves.append(Elf((i, row)))
            row += 1
    return elves

def move(elves: list[Elf], count):
    directions = ['n', 's', 'w', 'e']

    elf_map = ElfMap(elves)
    #elf_map.debug_print()

    i = 0
    while True:
        new_pos_to_elf = defaultdict(list)
        for elf in elves:
            if elf_map.has_adjacent_elf(elf):
                elf_move = calc_move(elf, elf_map, directions)
                if elf_move is not elf.position:
                    new_pos_to_elf[elf_move].append(elf)
        
        for new_pos, potential_elves in new_pos_to_elf.items():
            if len(potential_elves) > 1:
                continue
            elf_map.move(potential_elves[0], new_pos)

        #elf_map.debug_print()

        directions.append(directions.pop(0))
        
        if i == count - 1:
            pt1 = elf_map.get_empty_tiles()

        if len(new_pos_to_elf) == 0:
            pt2 = i
            break

        i += 1
    
    return pt1, pt2 + 1

def main():
    elves = parse('test.txt')
    pt1, pt2 = move(elves, 10)
    assert pt1 == 110
    assert pt2 == 20

    elves = parse('input.txt')
    pt1, pt2 = move(elves, 10)
    print(pt1)
    print(pt2)

if __name__ == '__main__':
    main()
