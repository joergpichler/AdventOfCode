def main():
    assert count_tiles('..^^.', 3) == 6
    assert count_tiles('.^^.^.^^^^', 10) == 38
    input = '^.....^.^^^^^.^..^^.^.......^^..^^^..^^^^..^.^^.^.^....^^...^^.^^.^...^^.^^^^..^^.....^.^...^.^.^^.^'
    tiles = count_tiles(input, 40)
    print(f'Pt1: {tiles} tiles')

    tiles = count_tiles(input, 400000)
    print(f'Pt2: {tiles} tiles')
    

def count_tiles(tile_row: str, total_rows: int):
    rows = [tile_row]

    while len(rows) < total_rows:
        rows.append(calc_next_row(rows[-1]))

    return sum(map(lambda x: x.count('.'), rows))


def calc_next_row(row: str):
    tiles = ''
    for i in range(len(row)):
        if i == 0:
            l = '.'
        else:
            l = row[i-1]
        c = row[i]
        if i == len(row) - 1:
            r = '.'
        else:
            r = row[i+1]
        
        tile = '.'
        if (l == '^' and c == '^' and not r == '^') or (c == '^' and r == '^' and not l == '^') or (l == '^' and not c == '^' and not r == '^') or (not l == "^" and not c == '^' and r == '^'):
            tile = '^'
        tiles += tile

    return tiles


if __name__ == '__main__':
    main()
