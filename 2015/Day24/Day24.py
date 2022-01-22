import itertools
import math
from typing import List

def parse(file):
    with open(file, 'r') as f:
        return [int(l.strip()) for l in f]

def _calc_min_qte(numbers: List[int], target_sum: int, depth: int, target_depth: int):
    
    if depth == target_depth:
        return True
    
    for i in range(1, len(numbers)):
        for c in (x for x in itertools.combinations(numbers, i) if sum(x) == target_sum):
            remaining_numbers = list(set(numbers)- set(c))
            if _calc_min_qte(remaining_numbers, target_sum, depth + 1, target_depth):
                return math.prod(c)
    
    return False

def calc_min_qte(numbers: List[int], split: int):
    target_sum = sum(numbers) / split
    if target_sum != int(target_sum):
        raise Exception()
    target_sum = int(target_sum)
    return _calc_min_qte(numbers, target_sum, 1, split)

def main():
    weights = parse('input.txt')
    print(f'Pt1: {calc_min_qte(weights, 3)}')
    print(f'Pt2: {calc_min_qte(weights, 4)}')

if __name__ == '__main__':
    main()
