import numpy as np

def parse(file):
    with open(file, 'r') as f:
        return np.array(list(map(lambda x: list(map(int, list(x.strip()))), f.readlines())), dtype=np.int8)   
    
def getNeighborIndices(matrix, index):
    for r in range(index[0] - 1, index[0] + 2):
        for c in range(index[1] - 1, index[1] + 2):
            if(r == index[0] and c == index[1]): # filter element itself
                continue
            if(r >= 0 and r < matrix.shape[0] and c >= 0 and c < matrix.shape[1]):
                yield(r, c)
    
def flash(matrix):
    matrix += 1
    
    flashing = np.where(matrix > 9)
    flashingIndices = list(zip(flashing[0], flashing[1]))
    flashingPtr = 0
    
    while len(flashingIndices) > flashingPtr:
        indexToFlash = flashingIndices[flashingPtr]
        neighborIndices = list(getNeighborIndices(matrix, indexToFlash))
        
        for neighborIndex in neighborIndices:
            if neighborIndex in flashingIndices:
                continue
            matrix[neighborIndex] += 1
            if(matrix[neighborIndex] > 9):
                flashingIndices.append(neighborIndex)
                
        flashingPtr += 1
    
    if(len(flashingIndices) > 0):
        #unzip indices list to get two vectors
        coordsToReset = list(zip(*flashingIndices))
        matrix[coordsToReset] = 0
    
    return len(flashingIndices)
    
def part1(matrix):
    sumOfFlashes = 0
    for i in range(100):
        sumOfFlashes += flash(matrix)
        
    print(f'Pt1: {sumOfFlashes} flashes')
    
def part2(matrix):
    
    noOfFlashes = 0
    i = 0
    
    while matrix.size > noOfFlashes:
        noOfFlashes = flash(matrix)
        i += 1
    
    print(f'Pt2: {i}')

def main():
    file = 'input.txt'
    matrix = parse(file)
    
    part1(matrix)
    
    matrix = parse(file)
    
    part2(matrix)

if __name__ == '__main__':
    main()