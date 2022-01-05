import re
from time import time


class Area:
    def __init__(self, x_min, x_max, y_min, y_max) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


def parse(file):
    with open(file, 'r') as f:
        match = re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', f.readline())
        x_bound_1 = int(match.group(1))
        x_bound_2 = int(match.group(2))
        y_bound_1 = int(match.group(3))
        y_bound_2 = int(match.group(4))

        return Area(min(x_bound_1, x_bound_2), max(x_bound_1, x_bound_2), min(y_bound_1, y_bound_2),
                    max(y_bound_1, y_bound_2))


def gaussian_sum(n):
    return int((n ** 2 + n) / 2)


def hits_target_area(v_x, v_y, area):
    p_x = 0
    p_y = 0
    while True:
        p_x += v_x
        p_y += v_y

        if p_y < area.y_min or p_x > area.x_max:
            return False

        if area.x_min <= p_x <= area.x_max and \
                area.y_min <= p_y <= area.y_max:
            return True

        v_x = v_x - 1 if v_x > 0 else 0
        v_y = v_y - 1


def main():
    file = 'input.txt'
    area = parse(file)

    if file == 'test.txt':
        assert hits_target_area(7, 2, area) is True
        assert hits_target_area(6, 3, area) is True
        assert hits_target_area(9, 0, area) is True
        assert hits_target_area(17, -4, area) is False
        assert hits_target_area(6, 9, area) is True

    y_max = 0
    velocities = []

    t0 = time()

    for x in range(1, area.x_max):
        for y in range(area.y_min, 1000):
            if hits_target_area(x, y, area):
                velocities.append((x, y))
                if y > y_max:
                    y_max = y

    t1 = time()

    print(f'Pt1: {gaussian_sum(y_max)}')
    print(f'Pt2: {len(velocities)}')
    print(f'{t1 - t0}')


if __name__ == '__main__':
    main()
