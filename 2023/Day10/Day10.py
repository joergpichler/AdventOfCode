import numpy as np

class Maze:
    def __init__(self, arr) -> None:
        self.arr = arr

    def get_start_tile(self):
        start = np.where(self.arr == 'S')
        row_start = start[0][0]
        col_start = start[1][0]
        assert self.arr[(row_start, col_start)] == 'S'
        return self.get_tile((row_start, col_start))
    
    def get_tile(self, coord):
        row = coord[0]
        if row < 0 or row > self.arr.shape[0]:
            return None
        col = coord[1]
        if col < 0 or col > self.arr.shape[1]:
            return None
        return Tile(self.arr[coord], coord)

class Tile:
    def __init__(self, shape, coord) -> None:
        if shape not in ['|', '-', 'L', 'J', '7', 'F', 'S', '.']:
            raise Exception
        self.shape = shape
        self.coord = coord

    def __repr__(self) -> str:
        return f'{self.shape} {self.coord}'
    
    def _get_connections(self):
        match self.shape:
            case '|':
                return ('N', 'S')
            case '-':
                return ('E', 'W')
            case 'L':
                return ('N', 'E')
            case 'J':
                return ('N', 'W')
            case '7':
                return ('S', 'W')
            case 'F':
                return ('S', 'E')
            case '.':
                return ()
            case _:
                raise Exception

    def get_exit(self, enter_from):
        connections = self._get_connections()
        if len(connections) == 0:
            return None
        if connections[0] == enter_from:
            return connections[1]
        elif connections[1] == enter_from:
            return connections[0]
        else:
            raise Exception

def parse(file):    
    with open(file, 'r') as f:
        rows = [list(x.strip()) for x in f]
    return Maze(np.array(rows))

def find_exit(tile, maze):

    directions = ['N', 'E', 'S', 'W']
    for direction in directions:
        try:
            next_tile = get_next_tile(tile, direction, maze)
            next_tile.get_exit(inverse_direction(direction))
            break
        except:
            pass

    return direction, next_tile

def get_next_tile(tile, direction, maze):
    d_r = -1 if direction == 'N' else (1 if direction == 'S' else 0)
    d_c = -1 if direction == 'W' else (1 if direction == 'E' else 0)

    next_tile = maze.get_tile((tile.coord[0] + d_r, tile.coord[1] + d_c))

    if next_tile is not None and next_tile.shape != '.':
        return next_tile
    
    raise Exception

def inverse_direction(direction):
    match direction:
        case 'N':
            return 'S'
        case 'E':
            return 'W'
        case 'S':
            return 'N'
        case 'W':
            return 'E'
        case _:
            raise Exception

def pt1(maze: Maze):
    tiles = []
    start_tile = maze.get_start_tile()
    direction, next_tile = find_exit(start_tile, maze)
    tiles.append(next_tile)

    while next_tile.shape != 'S':
        direction = next_tile.get_exit(inverse_direction(direction)) # enter the tile from the other direction
        next_tile = get_next_tile(next_tile, direction, maze)
        tiles.append(next_tile)
        pass

    return int(len(tiles) / 2)

def main():
    maze = parse('test.txt')
    assert pt1(maze) == 4
    maze = parse('test2.txt')
    assert pt1(maze) == 8
    maze = parse('input.txt')
    print(pt1(maze))    

if __name__ == '__main__':
    main()
