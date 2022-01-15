# https://stackoverflow.com/questions/4632322/finding-all-possible-combinations-of-numbers-to-reach-a-given-sum
# https://www.youtube.com/watch?v=NdF1QDTRkck

def parse(file):
    with open(file, 'r') as f:
        return [int(l.strip()) for l in f]

def subset_sum(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)

def count_subsets(numbers, target):
    sums = list(subset_sum(numbers, target))
    return len(sums)

def count_min_subsets(numbers, target):
    sums = list(subset_sum(numbers, target))
    min_len = min([len(s) for s in sums])
    return sum([1 for s in sums if len(s) == min_len])

def main():
    assert count_subsets([3, 1, 2, 1], 3) == 3
    assert count_subsets([20, 15, 10, 5, 5], 25) == 4
    
    numbers = parse('input.txt')
    
    print(f'Pt1: {count_subsets(numbers, 150)}')
    
    assert count_min_subsets([3, 1, 2, 1], 3) == 1
    assert count_min_subsets([20, 15, 10, 5, 5], 25) == 3
    
    print(f'Pt2: {count_min_subsets(numbers, 150)}')
    
    pass

if __name__ == '__main__':
    main()
