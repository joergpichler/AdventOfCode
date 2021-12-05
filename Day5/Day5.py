import re
import numpy as np

def parseInput():
    with open('input.txt', 'r') as f:
        matches = map(lambda x: re.match(r"(\d+),(\d+)\s->\s(\d+),(\d+)", x) ,f.readlines())
        tuples = map(lambda x: [tuple(map(int, x.group(1,2))), tuple(map(int, x.group(3,4)))], matches)
        return list(tuples)

def getMax(vectors, dim):
    result = 0
    for vector in vectors:
        result = max(result, vector[0][dim])
        result = max(result, vector[1][dim])
    return result

def spanMatrix(vectors):
    maxX = getMax(vectors, 0)
    maxY = getMax(vectors, 1)
    
    matrix = np.zeros((maxX + 1, maxY + 1), dtype=np.int8)
    
    return matrix

def markLines(matrix, vectors, alsoDiagonal: bool):
    for vector in vectors:
        x1 = vector[0][0]
        x2 = vector[1][0]
        y1 = vector[0][1]
        y2 = vector[1][1]
        
        # line in y dir (vertical)
        if(x1 == x2):
            x = x1
            minY = min(y1, y2)
            maxY = max(y1, y2)
            for y in range(minY, maxY + 1):
                matrix[(x, y)] += 1
            
        # line in x dir (horizontal)
        elif(y1 == y2):
            y = y1
            minX = min(x1, x2)
            maxX = max(x1, x2)
            for x in range(minX, maxX + 1):
                matrix[(x, y)] += 1
        
        # diagonal
        elif alsoDiagonal:
            dx = x2 - x1
            dy = y2 - y1
            if(abs(dx) != abs(dy)):
                raise Exception
            incX = int(dx / abs(dx))
            incY = int(dy / abs(dy))
            
            for i in range(0, abs(dx) + 1):
                matrix[(x1 + i * incX, y1 + i * incY)] += 1
            
def main():
    vectors = parseInput()
    
    matrix = spanMatrix(vectors)
    markLines(matrix, vectors, False)
    
    #print(matrix.transpose())
    
    count = (matrix >= 2).sum()
    print(count)
    
    matrix = spanMatrix(vectors)
    markLines(matrix, vectors, True)
    
    print(matrix.transpose())
    
    count = (matrix >= 2).sum()
    print(count)

if __name__ == '__main__':
    main()