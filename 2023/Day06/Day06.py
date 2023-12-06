import regex as re

def parse(file):
    with open(file, 'r') as f:
        for i  in range(2):
            if i == 0:
                times = [int(x) for x in re.findall(r'\d+', f.readline())]
            elif i == 1:
                distances = [int(x) for x in re.findall(r'\d+', f.readline())]
    return times, distances

def count_race_wins(time, distance):
    wins = 0
    for i in range(1, time):
        current_distance = i * (time - i)
        if current_distance > distance:
            wins = wins + 1
    return wins

def pt1(times, distances):
    result = 1
    for i in range(len(times)):
        result = result * count_race_wins(times[i], distances[i])
    return result

def pt2(times, distances):
    time = int(''.join([str(x) for x in times]))
    distance = int(''.join([str(x) for x in distances]))
    return count_race_wins(time, distance)

def main():
    times, distances = parse('test.txt')
    assert pt1(times, distances) == 288
    assert pt2(times, distances) == 71503
    
    times, distances = parse('input.txt')
    print(pt1(times, distances))
    print(pt2(times, distances))

if __name__ == '__main__':
    main()
