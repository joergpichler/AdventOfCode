import regex as re

def parse(file):
    with open(file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        return lines

def part1(lines):
    total = 0
    for line in lines:
        digits = re.findall(r'\d', line)
        d1 = digits[0]
        d2 = digits[-1]
        num = int(d1 + d2)
        total = total + num
    return total

def part2(lines):

    def to_int(s):
        int_strings = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        if s in int_strings:
            return int_strings.index(s) + 1
        return int(s)
    
    total = 0
    for line in lines:
        digits = re.findall(r'\d|one|two|three|four|five|six|seven|eight|nine', line, overlapped=True)
        d1 = to_int(digits[0])
        d2 = to_int(digits[-1])
        num = int(str(d1) + str(d2))
        total = total + num
    return total

def main():
    assert part1(parse('test.txt')) == 142
    print(part1(parse('input.txt')))
    
    assert part2(parse('test2.txt')) == 281
    print(part2(parse('input.txt')))

if __name__ == '__main__':
    main()
