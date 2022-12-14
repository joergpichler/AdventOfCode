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


    def get_points(self):
        for i in range(len(self._path) - 1):
            p1 = self._path[i]
            p2 = self._path[i + 1]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            if dx == 0 and dy != 0:
                min_y = min(p1[1], p2[1])
                max_y = max(p1[1], p2[1])
                for i in range(min_y, max_y + 1):
                    yield (p1[0], i)
            elif dy == 0 and dx != 0:
                min_x = min(p1[0], p2[0])
                max_x = max(p1[0], p2[0])
                for i in range(min_x, max_x + 1):
                    yield (i, p1[1])
            else:
                raise Exception


def parse(file):
    paths = set()
    with open(file, 'r') as f:
        for l in f:
            path = Path(l.strip())
            for p in path.get_points():
                paths.add(p)
    return paths


def is_blocked(pos, sand_set, paths):
    if pos in sand_set:
        return True
    if pos in paths:
        return True
    return False


def flow_sand(sand_pos, sand_set, paths, abyss_pos, part):
    while True:
        if part == 1 and sand_pos[1] >= abyss_pos:
            return False

        if part == 2 and sand_pos[1] + 1 == abyss_pos:
            sand_set.add(sand_pos)
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
    abyss = max((p[1] for p in paths))
    sand = set()

    while flow_sand((500, -1), sand, paths, abyss, 1):
        pass

    return len(sand)


def simulate_pt2(paths):
    abyss = max((p[1] for p in paths)) + 2
    sand = set()

    while (500, 0) not in sand:
        flow_sand((500, -1), sand, paths, abyss, 2)

    return len(sand)


def main():
    paths = parse('test.txt')
    assert simulate_pt1(paths) == 24
    assert simulate_pt2(paths) == 93
    
    paths = parse('input.txt')
    print(f'{simulate_pt1(paths)}')
    print(f'{simulate_pt2(paths)}')


if __name__ == '__main__':
    main()
