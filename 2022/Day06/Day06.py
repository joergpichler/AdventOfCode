def parse(file):
    with open(file, 'r') as f:
        return f.read().strip()

def find_marker(seq, chars = 4) -> int:
    for i in range(chars, len(seq) + 1):
        slice = seq[i-chars:i]
        if len(set(slice)) == chars:
            return i
    return -1

def main():
    assert find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
    assert find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
    assert find_marker('nppdvjthqldpwncqszvftbrmjlhg') == 6
    assert find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
    assert find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11

    assert find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
    assert find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
    assert find_marker('nppdvjthqldpwncqszvftbrmjlhg', 14) == 23
    assert find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) == 29
    assert find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26

    sequence = parse('input.txt')
    print(f'{find_marker(sequence)}')
    print(f'{find_marker(sequence, 14)}')
    
if __name__ == '__main__':
    main()
