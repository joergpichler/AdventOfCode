class Path:


    def __init__(self, s) -> None:
        self._path = Path._parse(s)
        self._validate()
        pass


    # check that no diagonals exist
    def _validate(self):
        for i in range(len(self._path) - 1):
            p1 = self._path[i]
            p2 = self._path[i + 1]
            if p2[0] - p1[0] != 0 and p2[1] - p1[1] != 0:
                raise Exception


    def _parse(s):
        path = []
        s = s.split(' -> ')
        for c in s:
            c = c.split(',')
            path.append((int(c[0]), int(c[1])))
        return path

    
    def __repr__(self) -> str:
        return str(self._path)


    @property
    def max_y(self):
        return max((p[1] for p in self._path))


    def contains(self, pos):
        for i in range(len(self._path) - 1):
            p1 = self._path[i]
            p2 = self._path[i + 1]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            if dx == 0 and p1[0] == pos[0]:
                min_y = min(p1[1], p2[1])
                max_y = max(p1[1], p2[1])
                if min_y <= pos[1] <= max_y:
                    return True
            if dy == 0 and p1[1] == pos[1]:
                min_x = min(p1[0], p2[0])
                max_x = max(p1[0], p2[0])
                if min_x <= pos[0] <= max_x:
                    return True
        return False


def parse(file):
    paths = []
    with open(file, 'r') as f:
        for l in f:
            paths.append(Path(l.strip()))
    return paths


def is_blocked(pos, sand_set, paths):
    if pos in sand_set:
        return True
    for p in paths:
        if p.contains(pos):
            return True
    return False


def flow_sand(sand_pos, sand_set, paths, abyss_pos):
    while True:
        if sand_pos[1] >= abyss_pos:
            return False

        down_pos = (sand_pos[0], sand_pos[1] + 1)
        if not is_blocked(down_pos, sand_set, paths):
            sand_pos = down_pos
            continue

        down_left_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
        if not is_blocked(down_left_pos, sand_set, paths):
            sand_pos = down_left_pos
            continue

        down_right_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
        if not is_blocked(down_right_pos, sand_set, paths):
            sand_pos = down_right_pos
            continue
        
        sand_set.add(sand_pos)

        return True


def simulate_pt1(paths):
    abyss = max((p.max_y for p in paths))
    sand = set()

    while flow_sand((500, -1), sand, paths, abyss):
        pass

    return len(sand)


def main():
    paths = parse('test.txt')
    assert simulate_pt1(paths) == 24
    
    paths = parse('input.txt')
    print(f'{simulate_pt1(paths)}')


if __name__ == '__main__':
    main()
