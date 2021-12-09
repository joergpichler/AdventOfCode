import numpy as np

def parse(file):
    with open(file, 'r') as f:
        return np.array(list(map(lambda x: list(map(int, list(x.strip()))), f.readlines())), dtype=np.int8)

def getNeighbors(matrix, index):
    for r in range(index[0] - 1, index[0] + 2):
        for c in range(index[1] - 1, index[1] + 2):
            if(r == index[0] and c == index[1]): # filter element itself
                continue
            if(r != index[0] and c != index[1]): # filter diagonals
                continue
            if(r >= 0 and r < matrix.shape[0] and c >= 0 and c < matrix.shape[1]):
                yield matrix[(r, c)]

def part1(heightMatrix):
    minimas = []
    riskLevelSum = 0
    it = np.nditer(heightMatrix, flags=['multi_index'])
    for x in it:
        neighbors = np.array(list(getNeighbors(heightMatrix, it.multi_index)))
        if((neighbors > x).all()):
            minimas.append(it.multi_index)
            riskLevelSum += x + 1
            #print(f'local minima {x} found at {it.multi_index}')
    
    print(f"Pt1: {riskLevelSum}")
    
    return minimas

def getBasinSize(heightMatrix, idx, indicesVisited):  
    if(idx in indicesVisited):
        return 0
    
    indicesVisited.append(idx)
    
    if(idx[0] < 0 or idx[1] < 0 or idx[0] >= heightMatrix.shape[0] or idx[1] >= heightMatrix.shape[1]): # stop out of bounds
        return 0
    
    if(heightMatrix[idx] == 9): # stop at 9
        return 0
    
    leftSize = getBasinSize(heightMatrix, (idx[0], idx[1] - 1), indicesVisited)
    topSize = getBasinSize(heightMatrix, (idx[0] - 1, idx[1]), indicesVisited)
    rightSize = getBasinSize(heightMatrix, (idx[0], idx[1] + 1), indicesVisited)
    bottomSize = getBasinSize(heightMatrix, (idx[0] + 1, idx[1]), indicesVisited)
    
    return 1 + leftSize + topSize + rightSize + bottomSize

def part2(heightMatrix, minimas):
    basinSizes = []
    for minima in minimas:
        basinSize = getBasinSize(heightMatrix, minima, [])
        basinSizes.append(basinSize)
    
    basinSizes = np.array(basinSizes)
    basinSizes.sort()
    
    print(f'Pt2: {np.prod(basinSizes[-3:])}')

def main():
    heightMatrix = parse('input.txt')
    
    minimas = part1(heightMatrix)
    
    part2(heightMatrix, minimas)

if __name__ == '__main__':
    main()