def get_code(target_row: int, target_col: int):
    code = 20151125
    target_coord = (target_row, target_col)
    coord = (1, 1)
    if coord == target_coord:
        return code
    row = 1

    while True:
        coord = (coord[0] - 1, coord[1] + 1)
        if coord[0] == 0:
            row += 1
            coord = (row, 1)
        code = (code * 252533) % 33554393
        if coord == target_coord:
            return code

def main():
    assert get_code(1, 1) == 20151125
    assert get_code(6, 6) == 27995004
    code = get_code(3010, 3019)
    print(code)

if __name__ == '__main__':
    main()
