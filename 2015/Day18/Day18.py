class LightsGrid:
    def __init__(self, lights: set, rows: int, cols: int) -> None:
        self.lights = lights
        self.rows = rows
        self.cols = cols
        self._stuck = False
        pass
    
    def flip(self):
        state = set()
        corners = set(self._get_corners())
        for row in range(self.rows):
            for col in range(self.cols):
                coord = (row, col)
                if self._stuck and coord in corners:
                    continue
                is_on = coord in self.lights
                on_neighbor_cnt = sum(self._get_neighbors(coord))
                if is_on and on_neighbor_cnt in [2, 3]:
                    state.add(coord)
                elif not is_on and on_neighbor_cnt == 3:
                    state.add(coord)
        if self._stuck:
            for c in self._get_corners():
                state.add(c)
        self.lights = state
        pass
    
    def _get_neighbors(self, coord):
        for row in range(coord[0] - 1, coord[0] + 2):
            for col in range(coord[1] - 1, coord[1] + 2):
                if row == coord[0] and col == coord[1]:
                    continue
                if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
                    yield False
                else:
                    yield (row, col) in self.lights
    
    def set_corners_stuck(self):
        self._stuck = True
        for c in self._get_corners():
            self.lights.add(c)
        
    def _get_corners(self):
        return [(0,0), (0, self.cols-1), (self.rows-1, 0), (self.rows-1, self.cols-1)]
    
    @property
    def lights_on(self):
        return len(self.lights)

def parse(file):
    lights = set()
    row_ctr = 0
    col_ctr = 0
    with open(file, 'r') as f:
        for line in f:
            col_ctr = max([col_ctr, len(line.strip())])
            for i in range(len(line)):
                c = line[i]
                if c == '#':
                    lights.add((row_ctr, i))
            row_ctr += 1
    return LightsGrid(lights, row_ctr, col_ctr)

def main():
    grid = parse('test.txt')
    for _ in range(4):
        grid.flip()
    assert grid.lights_on == 4
    
    grid = parse('input.txt')
    for _ in range(100):
        grid.flip()
    print(f'Pt1: {grid.lights_on}')
    
    grid = parse('test.txt')
    assert grid.lights_on != 17
    grid.set_corners_stuck()
    assert grid.lights_on == 17
    for _ in range(5):
        grid.flip()
    assert grid.lights_on == 17
    
    grid = parse('input.txt')
    grid.set_corners_stuck()
    for _ in range(100):
        grid.flip()
    print(f'Pt2: {grid.lights_on}')

if __name__ == '__main__':
    main()
