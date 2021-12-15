import numpy as np
from collections import defaultdict
from datetime import datetime

def parse(file):
    matrix = []
    with open(file, 'r') as f:
        for line in f:
            matrix.append([int(c) for c in line.strip()])
    return np.array(matrix)


def getInf():
    return np.inf

def getNextNodes(index, matrix):
    for r in range(index[0] - 1, index[0] + 2):
        for c in range(index[1] - 1, index[1] + 2):
            if(r == index[0] and c == index[1]): # filter element itself
                continue
            if(r != index[0] and c != index[1]): # filter diagonals
                continue
            if(r >= 0 and r < matrix.shape[0] and c >= 0 and c < matrix.shape[1]):
                yield (r, c)

def djikstra(matrix):
    costs = defaultdict(getInf)
    costs[(0,0)] = 0
    predecessors = {(0,0): None}
    queue = [(0,0)]
    visited = set()
    
    while len(queue) > 0:
        currentNode = queue[0]
        for queuedNode in queue:
            if queuedNode in visited:
                raise Exception
            if costs[queuedNode] < costs[currentNode]:
                currentNode = queuedNode
        queue.remove(currentNode)
        
        visited.add(currentNode)
        
        nextNodes = list(getNextNodes(currentNode, matrix))
        
        for nextNode in nextNodes:
            if nextNode in visited:
                continue
            
            cost = costs[currentNode] + matrix[nextNode]
            if costs[nextNode] > cost:
                costs[nextNode] = cost
                predecessors[nextNode] = currentNode
            if not nextNode in queue:
                queue.append(nextNode)
        
        if currentNode == (matrix.shape[0]-1, matrix.shape[1]-1):
            break
    
    #if len(visited) != matrix.size:
    #    raise Exception

    return predecessors

def increaseRisk(matrix, riskIncrese):
    result = np.copy(matrix)
    
    for i in range(riskIncrese):
        result = result + 1
        result[result > 9] = 1
        
    return result

def reshape(matrix, dim):
    rowMatrices = []
    
    for iRow in range(dim):
        rowMatrix = increaseRisk(matrix, iRow)
        for iCol in range(1, dim):
            rowMatrix = np.append(rowMatrix, increaseRisk(matrix, iRow + iCol), axis=1)
        rowMatrices.append(rowMatrix)
        
    result = rowMatrices[0]
    
    for i in range(1, len(rowMatrices)):
        result = np.append(result, rowMatrices[i], axis=0)
    
    return result

def calcShortestDistance(matrix):
    predecessors = djikstra(matrix)
    target = (matrix.shape[0]-1, matrix.shape[1]-1)
    
    sum = 0
    while(predecessors[target] is not None):
        sum += matrix[target]
        target = predecessors[target]
        
    print(sum)

def main():
    matrix = parse('input.txt')
    start = datetime.now()
    calcShortestDistance(matrix)
    end = datetime.now()
    print(f'Pt1 took {str(end-start)}')
    
    matrix = reshape(matrix, 5)
    
    start = datetime.now()
    calcShortestDistance(matrix)
    end = datetime.now()
    print(f'Pt2 took {str(end-start)}')
    
if __name__ == '__main__':
    main()