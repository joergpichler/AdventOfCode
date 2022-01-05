import numpy as np

def tick(fishes):
    fishdiff = np.array([0 for i in range(9)], dtype=np.int64)
    
    for i in range(9):
        if(i == 0):
            fishdiff[0] -= fishes[0]
            fishdiff[6] += fishes[0]
            fishdiff[8] += fishes[0]
        else:
            fishdiff[i-1] += fishes[i]
            fishdiff[i] -= fishes[i]
    
    return fishes + fishdiff

def parseFishes(inputFile):
    fishes = [0 for i in range(9)]
        
    with open(inputFile) as f:
        for initialTimer in map(int, f.readline().split(',')):
            fishes[initialTimer] += 1
    return np.array(fishes, dtype=np.int64)
        
def main():
    fishes = parseFishes('input.txt')
    
    for i in range(0, 80):
        fishes = tick(fishes)
            
    print(f'Pt1: After 80 days there are {np.sum(fishes)} fishes')
    
    for i in range(80, 256):
        fishes = tick(fishes)
    
    print(f'Pt1: After 256 days there are {np.sum(fishes)} fishes')

if __name__ == "__main__":
    main()