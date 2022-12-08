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

def determine_scenic_score(data):
    def determine_score(data, row, col):
        # edges
        if row == 0 or col == 0 or row == data.shape[0] - 1 or col == data.shape[1] - 1:
            return 0
        
        height = data[row, col]
        
        # left
        score_left = 0
        for i_row in range(row - 1, -1, -1):
            score_left += 1
            if data[i_row, col] >= height:
                break
        
        # top
        score_top = 0
        for i_col in range(col - 1, -1, -1):
            score_top += 1
            if data[row, i_col] >= height:
                break

        # right
        score_right = 0
        for i_row in range(row + 1, data.shape[1]):
            score_right += 1
            if data[i_row, col] >= height:
                break

        # top
        score_bottom = 0
        for i_col in range(col + 1, data.shape[0]):
            score_bottom += 1
            if data[row, i_col] >= height:
                break
        
        return score_left * score_top * score_right * score_bottom

    max_score = 0
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            max_score = max(max_score, determine_score(data, row, col))
            
    return max_score

def main():
    data = parse('test.txt')
    assert determine_visible_count(data) == 21
    assert determine_scenic_score(data) == 8

    data = parse('input.txt')
    print(f'{determine_visible_count(data)}')
    print(f'{determine_scenic_score(data)}')

if __name__ == '__main__':
    main()
