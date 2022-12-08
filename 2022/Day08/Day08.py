import numpy as np

def parse(file):
    return np.genfromtxt(file, delimiter=1, dtype=np.int8)

def determine_visible_count(data):
    visibilities = np.full(data.shape, False)

    def determine_visibility(data, row, col, current_max, visibilities):
        height = data[row,col]
        if height > current_max:
            visibilities[row,col] = True
        return max(height, current_max)

    # rows from left & right
    for row in range(data.shape[0]):
        # left
        current_max = -1
        for col in range(data.shape[1]):
            current_max = determine_visibility(data, row, col, current_max, visibilities)
        # right
        current_max = -1
        for col in range(data.shape[1] - 1, -1, -1):
            current_max = determine_visibility(data, row, col, current_max, visibilities)

    # cols from top & bottom
    for col in range(data.shape[1]):
        # top
        current_max = -1
        for row in range(data.shape[0]):
            current_max = determine_visibility(data, row, col, current_max, visibilities)
        # bottom
        current_max = -1
        for row in range(data.shape[0] - 1, -1, -1):
            current_max = determine_visibility(data, row, col, current_max, visibilities)

    return np.count_nonzero(visibilities)

def main():
    data = parse('test.txt')
    assert determine_visible_count(data) == 21

    data = parse('input.txt')
    print(f'{determine_visible_count(data)}')

if __name__ == '__main__':
    main()
