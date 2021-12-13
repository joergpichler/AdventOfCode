import numpy as np
import re

def parse(file):
    coords = []
    instructions = []
    
    with open(file, 'r') as f:
        for line in f:
            match = re.match(r'(\d+),(\d+)', line)
            if match:
                coords.append((int(match.group(2)), int(match.group(1))))
                continue
            match = re.match(r'fold along ([x|y])=(\d+)', line)
            if match:
                instructions.append((match.group(1), int(match.group(2))))
                continue
    
    maxRows = max(coords, key = lambda item: item[0])[0]
    maxCols = max(coords, key = lambda item: item[1])[1]
    
    matrix = np.zeros((maxRows + 1, maxCols + 1), dtype=np.int8)
    
    for coord in coords:
        matrix[coord] = 1
    
    return (matrix, instructions)

def foldRow(matrix, idxRow):
    if idxRow != (matrix.shape[0] - 1) / 2:
        raise Exception
    row = matrix[idxRow,:]
    if sum(row) != 0:
        raise Exception
    
    for iRow in range(idxRow + 1, matrix.shape[0]):
        for iCol in range(matrix.shape[1]):
            if matrix[iRow, iCol] == 1:
                matrix[idxRow - (iRow - idxRow), iCol] = 1
    
    return matrix[0:idxRow,:]

def foldColumn(matrix, idxCol):
    if idxCol != (matrix.shape[1] - 1) / 2:
        raise Exception
    col = matrix[:,idxCol]
    if sum(col) != 0:
        raise Exception
    
    for iCol in range(idxCol + 1, matrix.shape[1]):
        for iRow in range(matrix.shape[0]):
            if matrix[iRow, iCol] == 1:
                matrix[iRow, idxCol - (iCol - idxCol)] = 1
    
    return matrix[:,0:idxCol]

def fold(matrix, instruction):
    if instruction[0] == 'y':
        matrix = foldRow(matrix, instruction[1])
    elif instruction[0] == 'x':
        matrix = foldColumn(matrix, instruction[1])
    return matrix

def part1(matrix, instructions):
    matrix = fold(matrix, instructions[0])
    print(f'Pt1: {np.count_nonzero(matrix == 1)}')

def part2(matrix, instructions):
    for instruction in instructions:
        matrix = fold(matrix, instruction)
    
    str = ''
    for iRow in range(matrix.shape[0]):
        for iCol in range(matrix.shape[1]):
            str += '#' if matrix[iRow, iCol] == 1 else ' '
        str += '\n'
    print(str)

def main():
    matrix, instructions = parse('input.txt')

    part1(matrix, instructions)
    part2(matrix, instructions)

if __name__ == '__main__':
    main()