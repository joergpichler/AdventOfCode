import re
from collections import defaultdict

def parse(file):
    sensors = set()
    beacons = set()
    sensor_to_beacon = {}
    with open(file, 'r') as f:
        for l in f:
            matches = re.findall(r'x=(-?\d+), y=(-?\d+)', l.strip())
            if len(matches) != 2:
                raise Exception
            sensor = (int(matches[0][0]), int(matches[0][1]))
            beacon = (int(matches[1][0]), int(matches[1][1]))
            sensors.add(sensor)
            beacons.add(beacon)
            sensor_to_beacon[sensor] = beacon
    return sensors, beacons, sensor_to_beacon


def count_points_at_y(y, ranges, *args):
    result = set()
    for r in ranges:
        for i in r:
            result.add(i)
    for a in args:
        for i in a:
            if i[1] == y and i[0] in result:
                result.remove(i[0])
    return len(result)

def get_ranges_at_y(sensor_to_beacon, target_row):
    ranges = []
    for s, b in sensor_to_beacon.items():
        dx = abs(b[0] - s[0])
        dy = abs(b[1] - s[1])
        d = dx + dy

        if s[1] - d <= target_row <= s[1] + d:
            diff_y = abs(target_row - s[1])
        else:
            continue

        diff_x = d - diff_y

        ranges.append(range(s[0] - diff_x, s[0] + diff_x + 1))

    return ranges


def pt1(sensors, beacons, sensor_to_beacon, target_row):
    ranges = get_ranges_at_y(sensor_to_beacon, target_row)

    return count_points_at_y(target_row, ranges, sensors, beacons)


def pt2(sensors, beacons, sensor_to_beacon, max_row):
    pass

def main():
    sensors, beacons, sensor_to_beacon = parse('test.txt')
    assert pt1(sensors, beacons, sensor_to_beacon, 10) == 26
    #assert pt2(sensors, beacons, sensor_to_beacon, 20) == 56000011


    sensors, beacons, sensor_to_beacon = parse('input.txt')
    print(f'{pt1(sensors, beacons, sensor_to_beacon, 2000000)}')

if __name__ == '__main__':
    main()
