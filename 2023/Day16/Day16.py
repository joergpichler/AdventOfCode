import numpy as np

class Tile:
    def __init__(self, type) -> None:
        self.type = type
        self.energized = False
        self.encountered_beams = set()

    def __repr__(self) -> str:
        return f'{self.type} {self.energized}'

class Beam:
    def __init__(self, location, direction) -> None:
        self.location = location
        self.direction = direction

    def move(self, tile):
        tile.energized = True
        if tile.type == '.':
            self._move()
        elif tile.type == '|':
            if self.direction == 'u' or self.direction == 'd':
                self._move()
            else:                
                new_beam = Beam((self.location[0] + 1, self.location[1]), 'd')
                self.direction = 'u'
                self._move()
                return new_beam
        elif tile.type == '-':
            if self.direction == 'r' or self.direction == 'l':
                self._move()
            else:
                new_beam = Beam((self.location[0], self.location[1] + 1), 'r')
                self.direction = 'l'
                self._move()
                return new_beam
        elif tile.type == '/':
            if self.direction == 'r':
                self.direction = 'u'
            elif self.direction == 'd':
                self.direction = 'l'
            elif self.direction == 'l':
                self.direction = 'd'
            elif self.direction == 'u':
                self.direction = 'r'
            self._move()
        elif tile.type == '\\':
            if self.direction == 'r':
                self.direction = 'd'
            elif self.direction == 'd':
                self.direction = 'r'
            elif self.direction == 'l':
                self.direction = 'u'
            elif self.direction == 'u':
                self.direction = 'l'
            self._move()
        else:
            pass
            
        return None

    def _move(self):
        if self.direction == 'r':
            self.location = (self.location[0], self.location[1] + 1)
        elif self.direction == 'd':
            self.location = (self.location[0] + 1, self.location[1])
        elif self.direction == 'l':
            self.location = (self.location[0], self.location[1] - 1)
        elif self.direction == 'u':
            self.location = (self.location[0] - 1, self.location[1])

    def __repr__(self) -> str:
        return f'{self.location} {self.direction}'

def parse(file):
    with open(file, 'r') as f:
        return np.array([list(Tile(c) for c in l.strip()) for l in f])

def debug_print(data, beams):
    beam_set = set([x.location for x in beams])

    for row in range(data.shape[0]):
        row_str = ''
        for col in range(data.shape[1]):
            if (row, col) in beam_set:
                row_str += 'b'
            else:
                row_str += data[row, col].type
        print(row_str)
    
    print()

def count_energized_tiles(data):
    condition = np.array([[obj.energized for obj in row] for row in data], dtype=bool)
    count = np.count_nonzero(condition)
    return count

def simulate(data, initial_beam):
    def move_beams(beams, data):
        for i in range(len(beams)):
            beam = beams[i]
            tile = data[beam.location]
            tile.encountered_beams.add(beam.direction)
            new_beam = beam.move(tile)
            if new_beam is not None:
                beams.append(new_beam)

    beams = [initial_beam]

    while len(beams) > 0:
        #debug_print(data, beams)

        move_beams(beams, data)

        for i in range(len(beams) - 1, -1, -1):
            beam = beams[i]
            if beam.location[0] < 0 or beam.location[0] >= data.shape[0] or beam.location[1] < 0 or beam.location[1] >= data.shape[1]:
                del beams[i]
                continue
            tile = data[beam.location]
            if beam.direction in tile.encountered_beams:
                del beams[i]
                continue
    
    return count_energized_tiles(data)

def pt1(data):
    return simulate(data, Beam((0,0), 'r'))

def pt2(file):
    data = parse(file)
    rows = data.shape[0]
    columns = data.shape[1]

    result = 0
    
    # left
    column = 0
    for row in range(rows):
        data = parse(file)
        result = max(result, simulate(data, Beam((row, column), 'r')))
    # right
    column = columns - 1
    for row in range(rows):
        data = parse(file)
        result = max(result, simulate(data, Beam((row, column), 'l')))
    # down
    row = 0
    for column in range(columns):
        data = parse(file)
        result = max(result, simulate(data, Beam((row, column), 'd')))
    # up
    row = rows - 1
    for column in range(columns):
        data = parse(file)
        result = max(result, simulate(data, Beam((row, column), 'u')))
    
    return result

def main():
    data = parse('test.txt')
    assert pt1(data) == 46
    assert pt2('test.txt') == 51
    data = parse('input.txt')
    print(pt1(data))
    print(pt2('input.txt'))
    pass

if __name__ == '__main__':
    main()
