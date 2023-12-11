import numpy as np

class Space:
    def __init__(self, arr, expansion) -> None:
        arr = np.array(arr)
        self.galaxies = list(list(a) for a in zip(*np.where(arr == '#')))
        self._calc_column_expansion(arr, expansion)
        self._calc_row_expansion(arr, expansion)

    def _calc_row_expansion(self, arr, expansion):
        expanded_rows = []
        for i in range(arr.shape[0]):
            row = arr[i,:]
            if np.all(row == '.'):
                expanded_rows.append(i)
        expanded_rows = np.array(expanded_rows)
        for i in range(len(self.galaxies)):
            galaxy = self.galaxies[i]
            rows = np.sum(expanded_rows < galaxy[0])
            galaxy[0] = galaxy[0] + rows * (expansion - 1)

    def _calc_column_expansion(self, arr, expansion):
        expanded_cols = []
        for i in range(arr.shape[1]):
            col = arr[:,i]
            if np.all(col == '.'):
                expanded_cols.append(i)
        expanded_cols = np.array(expanded_cols)
        for i in range(len(self.galaxies)):
            galaxy = self.galaxies[i]
            cols = np.sum(expanded_cols < galaxy[1])
            galaxy[1] = galaxy[1] + cols * (expansion - 1)

def parse(file, expansion):
    with open(file, 'r') as f:
        arr = [list(x.strip()) for x in f]
    space = Space(arr, expansion)
    return space

def calc_distances(space):
    total = 0
    galaxy_indices = space.galaxies
    for i in range(len(galaxy_indices)):
        for j in range(i + 1, len(galaxy_indices)):
            source = galaxy_indices[i]
            target = galaxy_indices[j]
            d_r = target[0] - source[0]
            d_c = target[1] - source[1]
            steps = abs(d_r) + abs(d_c)
            total = total + steps
    return total

def main():
    space = parse('test.txt', 2)
    assert calc_distances(space) == 374
    space = parse('test.txt', 10)
    assert calc_distances(space) == 1030
    space = parse('test.txt', 100)
    assert calc_distances(space) == 8410
    space = parse('input.txt', 2)
    print(calc_distances(space))
    space = parse('input.txt', 1000000)
    print(calc_distances(space))

if __name__ == '__main__':
    main()
