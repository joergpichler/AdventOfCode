def parse(file):
    pixels = set()
    line_ctr = 0
    with open(file, 'r') as f:
        enhancement = f.readline().strip()
        f.readline()
        for line in f:
            for i in range(len(line)):
                c = line[i]
                if c == '#':
                    pixels.add((line_ctr, i))
            line_ctr += 1
    return enhancement, pixels


def get_max_row_col(pixels: set):
    max_row = max(pixels, key=lambda item: item[0])[0]
    max_col = max(pixels, key=lambda item: item[1])[1]
    return max_row + 1, max_col + 1


def get_binary(row, col, pixels, max_row, max_col, background):
    bin_str = ''
    for i_row in range(row - 1, row + 2):
        for i_col in range(col - 1, col + 2):
            if 0 <= i_row < max_row and 0 <= i_col < max_col:
                bin_str += '1' if (i_row, i_col) in pixels else '0'
            else:
                bin_str += str(background)
    return bin_str


def get_new_pixel(row, col, pixels, enhancement, max_row, max_col, background):
    binary = get_binary(row, col, pixels, max_row, max_col, background)
    return enhancement[int(binary, 2)]


def enhance_image(pixels, enhancement, background):
    max_row, max_col = get_max_row_col(pixels)
    new_pixels = set()

    for i_row in range(-1, max_row + 1):
        for i_col in range(-1, max_col + 1):
            if get_new_pixel(i_row, i_col, pixels, enhancement, max_row, max_col, background) == '#':
                new_pixels.add((i_row + 1, i_col + 1))

    return new_pixels


def debug_print(pixels):
    min_row, max_row, min_col, max_col = get_max_row_col(pixels)
    for i_row in range(max_row):
        row = ''
        for i_col in range(max_col):
            row += '#' if pixels[(i_row, i_col)] == 1 else '.'
        print(row)
    print('')


def main():
    enhancement, pixels = parse('input.txt')
    background_flip = enhancement[0] == '#' and enhancement[-1] == '.'
    background = 0

    for i in range(50):

        if background_flip:
            if i % 2 == 0:
                background = 0
            else:
                background = 1

        pixels = enhance_image(pixels, enhancement, background)

        if i == 1:
            print(f'Pt1: {len(pixels)}')

    print(f'Pt2: {len(pixels)}')


if __name__ == '__main__':
    main()
