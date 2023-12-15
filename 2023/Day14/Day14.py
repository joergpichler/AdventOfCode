import numpy as np

def parse(file):
    with open(file, 'r') as f:
        return np.array([list(x.strip()) for x in f])

def move_rocks(data):
    rocks_moved = False
    for i_row in range(data.shape[0] - 1): # skip last row
        for i_col in range(data.shape[1]):
            val = data[i_row, i_col]
            if val == '.' and data[i_row + 1, i_col] == 'O':
                rocks_moved = True
                data[i_row, i_col] = 'O'
                data[i_row + 1, i_col] = '.'

    return rocks_moved

def tilt(data, direction):
    match direction:
        case 'W':
            data = np.rot90(data, 3)
        case 'S':
            data = np.rot90(data, 2)
        case 'E':
            data = np.rot90(data, 1)
        case _:
            pass

    while(move_rocks(data)):
        pass

    match direction:
        case 'W':
            data = np.rot90(data, 1)
        case 'S':
            data = np.rot90(data, 2)
        case 'E':
            data = np.rot90(data, 3)
        case _:
            pass

    return data

def calc_load(data):
    load = 0
    for i in range(data.shape[0] - 1, -1, -1):
        value = data.shape[0] - i
        load = load + (sum((1 for x in data[i, :] if x == 'O')) * value)
    return load

def pt1(data):
    data = tilt(data, 'N')
    return calc_load(data)
    
def pt2(data):
    loads = []
    for i in range(1000000000):
        data = tilt(data, 'N')
        data = tilt(data, 'W')
        data = tilt(data, 'S')
        data = tilt(data, 'E')
        loads.append(calc_load(data))
        if i > 0 and i % 1000 == 0:
            cycle_start, cycle_length = find_cycle(loads)
            if cycle_start is not None:
                pass
    return loads[-1]

# chat gpt ftw
def find_cycle(nums):
    # Initialize two pointers, one slow (tortoise) and one fast (hare)
    tortoise = nums[0]
    hare = nums[0]

    # Move hare two steps at a time and tortoise one step at a time
    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]

        # If there is a cycle, the hare and tortoise will eventually meet
        if tortoise == hare:
            break

    # Find the start of the cycle
    tortoise = nums[0]
    while tortoise != hare:
        tortoise = nums[tortoise]
        hare = nums[hare]

    # The hare and tortoise will meet at the start of the cycle
    cycle_start = hare

    # Determine the length of the cycle
    cycle_length = 1
    hare = nums[hare]
    while hare != cycle_start:
        hare = nums[hare]
        cycle_length += 1

    return cycle_start, cycle_length

def main():

    data = parse('test.txt')
    assert pt1(data) == 136
    data = parse('test.txt')
    assert pt2(data) == 64
    data = parse('input.txt')
    print(pt1(data))
    data = parse('input.txt')
    print(pt2(data))

if __name__ == '__main__':
    main()
