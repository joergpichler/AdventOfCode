import numpy as np

class Map:
    def __init__(self, rows, cols, map) -> None:
        self.rows = rows
        self.cols = cols
        self.map = map
        pass
    
    def step(self):
        moves = []
        for source in [k for k,v in self.map.items() if v == '>']:
            target = self._next_e(source)
            if target not in self.map:
                moves.append((source, target))
            pass
        for m in moves:
            self.map.pop(m[0])
            self.map[m[1]] = '>'
        
        move_ctr = len(moves)
        moves.clear()
        
        for source in [k for k,v in self.map.items() if v == 'v']:
            target = self._next_s(source)
            if target not in self.map:
                moves.append((source, target))
            pass
        for m in moves:
            self.map.pop(m[0])
            self.map[m[1]] = 'v'
            
        move_ctr += len(moves)
        return move_ctr
    
    def _next_e(self, coords):
        return (coords[0], (coords[1] + 1) % self.cols)
    
    def _next_s(self, coords):
        return ((coords[0] + 1) % self.rows, coords[1])
    
    def print(self):
        for r in range(self.rows):
            str = ''
            for c in range(self.cols):
                if (r, c) in self.map:
                    str += self.map[(r,c)]
                else:
                    str += '.'
            print(str)

def parse(file):
    rows = 0
    cols = 0
    map = {}
    with open(file, 'r') as f:
        for line in f:
            chars = list(line.strip())
            for i in range(len(chars)):
                c = chars[i]
                if c == '>':
                    map[(rows, i)] = '>'
                    pass
                elif c == 'v':
                    map[(rows, i)] = 'v'
                    pass
            rows += 1
            cols = len(chars)
            pass
    return Map(rows, cols, map)

def main():
    map = parse('input.txt')
    steps = 0
    moving = 1
    while moving > 0:
        moving = map.step()
        steps += 1
    print(f'Pt1: {steps}')

if __name__ == '__main__':
    main()
