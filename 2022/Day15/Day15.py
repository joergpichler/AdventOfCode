import re
from multiprocessing import Pool


def parse(file):
    result = []
    with open(file, 'r') as f:
        for l in f:
            matches = re.findall(r'x=(-?\d+), y=(-?\d+)', l.strip())
            if len(matches) != 2:
                raise Exception
            sensor = (int(matches[0][0]), int(matches[0][1]))
            beacon = (int(matches[1][0]), int(matches[1][1]))
            result.append((sensor, beacon))
    return result


def count_points_at_y(y, ranges, sensors_and_beacons):
    result = set()
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            result.add(i)
    for s, b in sensors_and_beacons:
        if s[1] == y and s[0] in result:
            result.remove(s[0])
        if b[1] == y and b[0] in result:
            result.remove(b[0])
    return len(result)


def get_ranges_at_y(sensors_and_beacons, target_row):
    ranges = []
    for s, b in sensors_and_beacons:
        dx = abs(b[0] - s[0])
        dy = abs(b[1] - s[1])
        d = dx + dy

        if s[1] - d <= target_row <= s[1] + d:
            diff_y = abs(target_row - s[1])
        else:
            continue

        diff_x = d - diff_y

        ranges.append((s[0] - diff_x, s[0] + diff_x))

    return ranges


def pt1(sensors_and_beacons, target_row):
    ranges = get_ranges_at_y(sensors_and_beacons, target_row)

    return count_points_at_y(target_row, ranges, sensors_and_beacons)


def get_hole(ranges):
    s = sorted(ranges)
    current_max = s[0][1]
    for r in s[1:]:
        if r[1] <= current_max:
            continue
        if r[0] > current_max:
            return r[0] - 1
        current_max = r[1]
    return None


def task_pt2(row, sensor_to_beacon):
    ranges = get_ranges_at_y(sensor_to_beacon, row)
    x = get_hole(ranges)
    if x is not None:
        return x * 4000000 + row


def pt2(sensor_to_beacon, max_row):
    items = ((row, sensor_to_beacon) for row in range(0, max_row + 1))

    with Pool() as pool:
        for result in pool.starmap(task_pt2, items):
            if result is not None:
                return result


def main():
    sensors_and_beacons = parse('test.txt')
    assert pt1(sensors_and_beacons, 10) == 26
    assert pt2(sensors_and_beacons, 20) == 56000011

    sensors_and_beacons = parse('input.txt')
    print(f'{pt1(sensors_and_beacons, 2000000)}')
    print(f'{pt2(sensors_and_beacons, 4000000)}')


if __name__ == '__main__':
    main()