import sys
import numpy as np

def sumNaturalNumbers(n):
    return int(n * (n + 1) / 2)

def parse(file: str):
    with open(file, 'r') as f:
        return np.array(list(map(int, f.readline().split(','))))
    
def main():
    crabPos = parse('input.txt')
    
    min = crabPos.min()
    max = crabPos.max()
    
    minSum = sys.maxsize
    iFound = -1
    
    for i in range(min, max + 1):
        sum = np.abs(crabPos - i).sum()
        if sum < minSum:
            minSum = sum
            iFound = i
    
    print(f'Pt1: {iFound}: {minSum}')
    
    minSum = sys.maxsize
    iFound = -1
    
    for i in range(min, max + 1):
        abs = np.abs(crabPos - i)
        abs = np.array([sumNaturalNumbers(steps) for steps in abs])
        sum = abs.sum()
        if sum < minSum:
            minSum = sum
            iFound = i
    
    print(f'Pt2: {iFound}: {minSum}')

if __name__ == "__main__":
    main()