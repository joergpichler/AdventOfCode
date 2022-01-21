import itertools
import math
from typing import List

qte = -1
length = -1

def parse(file):
    with open(file, 'r') as f:
        return [int(l.strip()) for l in f]

def calc_qte(results, length):
    qte = -1
    for p in results:
        if len(p) != length:
            continue
        tmp_qte = math.prod(p)
        if qte == -1:
            qte = tmp_qte
        elif tmp_qte < qte:
            qte = tmp_qte
    assert qte != -1
    return qte

def calc(results):
    global length
    global qte

    min_len_results = min(len(x) for x in results)

    if min_len_results > length:
        return
    elif min_len_results == length:
        tmp_qte = calc_qte(results, min_len_results)
        if tmp_qte < qte:
            qte = tmp_qte
            print(qte)
    else:
        length = min_len_results
        qte = calc_qte(results, min_len_results)
        print(qte)

def find_combination(numbers: List[int], target_sum: int, depth: int, target_depth: int, results: List):
    if depth == target_depth:
        if sum(numbers) == target_sum:
            results.append(tuple(numbers))
            calc(results)
            return
        else:
            return

    for i in range(1, len(numbers)):
        for c in (x for x in itertools.combinations(numbers, i) if sum(x) == target_sum):
            cpy = results.copy()
            cpy.append(c)
            find_combination(list(set(numbers)- set(c)), target_sum, depth + 1, target_depth, cpy)

def main():
    weights = parse('input.txt')
    global length
    length = len(weights)
    target_weight = int(sum(weights) / 4)

    results = []
    find_combination(weights, target_weight, 1, 4, results)
    # for whatever reason the first result is already the optimum ???! just run it and cancel when the first number is printed :)

if __name__ == '__main__':
    main()
