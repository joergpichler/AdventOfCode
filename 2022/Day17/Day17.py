from typing import List
import numpy as np
from operator import itemgetter

class Rock:

    def __init__(self, shape: List[tuple[int, int]]) -> None:
        self._shape = shape

    def __repr__(self) -> str:
        x_max = max(map(itemgetter(0), self.shape))
        y_max = max(map(itemgetter(1), self.shape))
        arr = np.full((y_max + 1, x_max + 1), False)
        for p in self.shape:
            arr[y_max - p[1], p[0]] = True
        return arr.__repr__()

    @property
    def shape(self):
        return list(self._shape)


class RockFactory:

    def __init__(self) -> None:
        a = [(0,0),(1,0),(2,0),(3,0)] # horizontal shape
        b = [(1,0),(0,1),(1,1),(2,1),(1,2)] # plus shape
        c = [(0,0),(1,0),(2,0),(2,1),(2,2)] # reverse L shape
        d = [(0,0),(0,1),(0,2),(0,3)] # I shape
        e = [(0,0),(1,0),(0,1),(1,1)] # square shape
        self._patterns = [a,b,c,d,e]
    
    def get_rock(self, index):
        return Rock(self._patterns[index])

    @property
    def rock_count(self):
        return len(self._patterns)


class PushFactory:
    def __init__(self, pattern_str: str) -> None:
        self._pattern = list(pattern_str)
        self._index = 0

    def get_next(self):
        result = self._pattern[self._index % len(self._pattern)]
        self._index += 1
        return result


class Chamber:
    def __init__(self, push_factory: PushFactory) -> None:
        self._push_factory = push_factory
        self.blocked_tiles = set()
        
    @property
    def max_y(self):
        return max(map(itemgetter(1), self.blocked_tiles)) if len(self.blocked_tiles) > 0 else 0

    def _place_rock(self, rock: Rock):
        d_y = self.max_y + 3 + 1 # 0 is the floor
        d_x = 2 + 1 # 0 is the wall
        return list(map(lambda p: (p[0] + d_x, p[1] + d_y), rock.shape))

    def _push_rock(self, rock_pos: List[tuple[int, int]], push_direction: str):
        if push_direction == '>': # right
            d_x = 1
        elif push_direction == '<': # left:
            d_x = -1
        else:
            raise Exception
        tmp_pos = list(map(lambda p: (p[0] + d_x, p[1]), rock_pos))
        for p in tmp_pos:
            if p in self.blocked_tiles:
                return rock_pos
            if p[0] == 0 or p[0] == 8:
                return rock_pos
        return tmp_pos
        
    def _fall_rock(self, rock_pos: List[tuple[int, int]]):
        d_y = -1
        tmp_pos = list(map(lambda p: (p[0], p[1] + d_y), rock_pos))
        for p in tmp_pos:
            if p in self.blocked_tiles:
                return rock_pos
            if p[1] == 0:
                return rock_pos
        return tmp_pos

    def insert_rock(self, rock: Rock):
        rock_pos = self._place_rock(rock)
        rock_pos = self._push_rock(rock_pos, self._push_factory.get_next())
        while True:
            next_pos = self._fall_rock(rock_pos)
            if next_pos is rock_pos:
                self.blocked_tiles.update(rock_pos)
                return
            rock_pos = next_pos
            rock_pos = self._push_rock(rock_pos, self._push_factory.get_next())
    
    def __repr__(self) -> str:
        s = ''
        for r in range(self.max_y, 0, -1):
            r_s = ''
            for c in range(1,8):
                if (c, r) in self.blocked_tiles:
                    r_s += '#'
                else:
                    r_s += '.'
            s += r_s
            s += "\n"
        return s


def parse(file: str) -> str:
    with open(file, 'r') as f:
        line = f.readline().strip()
        return line

def find_pattern(chamber: Chamber):
    max_y = chamber.max_y

    for i in range(10, max_y // 2): # start at 10 because otherwise 2 identical lines become a pattern
        upper_part = np.zeros((i + 1, 7), dtype=np.int8)

        for r in range(max_y, max_y - i - 1, -1):
            for c in range(1, 8):
                if (c, r) in chamber.blocked_tiles:
                    upper_part[max_y - r, c - 1] = 1
        
        lower_part = np.zeros((i + 1, 7), dtype=np.int8)

        for r in range(max_y - i - 1, max_y - i - 1 - i - 1, -1):
            for c in range(1, 8):
                if (c, r) in chamber.blocked_tiles:
                    lower_part[max_y - i - 1 - r, c - 1] = 1


        if np.array_equal(upper_part, lower_part):
            print('pattern found')

    return



def run_sim(pattern: str, count_rocks: int, part2: bool = False):
    rock_factory = RockFactory()
    chamber = Chamber(PushFactory(pattern))

    rock_idx = 0
    for _ in range(count_rocks):
        rock = rock_factory.get_rock(rock_idx)
        rock_idx += 1
        if rock_idx == rock_factory.rock_count:
            rock_idx = 0
        chamber.insert_rock(rock)

        if part2:
            find_pattern(chamber)
            pass # try to find a repeating pattern

    return chamber.max_y

def main():
    pattern = parse('test.txt')
    #assert run_sim(pattern, 2022) == 3068
    #assert run_sim(pattern, 1000000000000, True) == 1514285714288

    pattern = parse('input.txt')
    #print(f'{run_sim(pattern, 2022)}')
    print(f'{run_sim(pattern, 1000000000000, True)}')


if __name__ == '__main__':
    main()
