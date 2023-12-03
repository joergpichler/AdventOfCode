import numpy as np
import regex as re

def parse(file):
    lines = []
    with open(file, 'r') as f:
        for l in (x.strip() for x in f):
            lines.append(list(l))
            
    return np.array(lines)

def pt1(data):

    total = 0

    def has_symbol_adjacent(data, row, col):
        for d_r in range(-1, 2):
            for d_c in range(-1, 2):
                if d_r == 0 and d_c == 0:
                    continue
                r = row + d_r
                c = col + d_c

                if r < 0 or r > data.shape[0] - 1:
                    continue
                if c < 0 or c > data.shape[1] - 1:
                    continue

                e = data[r, c]

                if re.match(r'[^0-9\.]', e):
                    return True
                
        return False
    
    for row in range(0, data.shape[0]):

        num = []
        symbol = False

        for col in range(0, data.shape[1]):
            c = data[row, col]
            if re.match(r'[0-9]', c):
                num.append(c)
                if not symbol:
                    symbol = has_symbol_adjacent(data, row, col)
            else:
                if symbol:
                    total = total + int(''.join(num))
                num = []
                symbol = False
        
        if symbol:
            total = total + int(''.join(num))

    return total

def pt2(data):

    def get_num_at(data, coord):
        row = coord[0]
        column = coord[1]
        num_str = data[coord]
        for c in range(column - 1, -1, -1):
            e = data[row, c]
            if re.match(r'\d', e):
                num_str = e + num_str
            else:
                break
        for c in range(column + 1, data.shape[1]):
            e = data[row, c]
            if re.match(r'\d', e):
                num_str = num_str + e
            else:
                break
        return int(num_str)

    def get_adjacent_numbers(data, row, col):
        nums = []
        for d_r in range(-1, 2):
            match = None
            for d_c in range(-1, 2):
                if d_r == 0 and d_c == 0:
                    if match is not None:
                        nums.append(get_num_at(data, match))
                    match = None
                r = row + d_r
                c = col + d_c

                if r < 0 or r > data.shape[0] - 1:
                    continue
                if c < 0 or c > data.shape[1] - 1:
                    continue

                e = data[r, c]

                if re.match(r'[0-9]', e):
                    match = (r, c)
                else:
                    if match is not None:
                        nums.append(get_num_at(data, match))
                    match = None
            
            if match is not None:
                nums.append(get_num_at(data, match))

        return nums

    total = 0
    for row in range(0, data.shape[0]):
        for col in range(0, data.shape[1]):
            c = data[row, col]
            if c == '*':
                nums = get_adjacent_numbers(data, row, col)
                if len(nums) == 2:
                    ratio = nums[0] * nums[1]
                    total = total + ratio
    return total

def main():
    data = parse('test.txt')
    assert pt1(data) == 4361
    assert pt2(data) == 467835

    data = parse('input.txt')
    print(pt1(data))
    print(pt2(data))

if __name__ == '__main__':
    main()
