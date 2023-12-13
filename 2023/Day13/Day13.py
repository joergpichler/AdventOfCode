import numpy as np

class Pattern:
    def __init__(self, lines) -> None:
        self.lines = np.array(lines)

    def __repr__(self) -> str:
        return self.lines.__repr__()
    
    @staticmethod
    def _to_bin(c):
        if c == '#':
            return '1'
        elif c == '.':
            return '0'
        raise Exception

    def get_column_hashes(self):
        binaries = []
        for c in range(self.lines.shape[1]):
            column = self.lines[:,c]
            binary = int(''.join(map(Pattern._to_bin, column)), 2)
            binaries.append(binary)
        return binaries
    
    def get_row_hashes(self):
        binaries = []
        for r in range(self.lines.shape[0]):
            row = self.lines[r,:]
            binary = int(''.join(map(Pattern._to_bin, row)), 2)
            binaries.append(binary)
        return binaries

def parse(file):
    patterns = []
    lines = []
    with open(file, 'r') as f:
        for l in f:
            l = l.strip()
            if l:
                lines.append(list(l))
            else:
                patterns.append(Pattern(lines))
                lines = []
    patterns.append(Pattern(lines))
    return patterns

def is_reflection_pt1(hashes, i):
        left = i - 1
        right = i
        while left >= 0 and right < len(hashes):
            if hashes[left] != hashes[right]:
                return False
            left = left - 1
            right = right + 1
            if left < 0 or right > len(hashes) - 1:
                break
        return True

def is_reflection_pt2(hashes, i):
    def is_smudge(left, right):
        left_bin = "{0:b}".format(left)
        right_bin = "{0:b}".format(right)
        fill = max(len(left_bin), len(right_bin))
        left_bin = left_bin.zfill(fill)
        right_bin = right_bin.zfill(fill)
        return sum((1 for x in zip(left_bin, right_bin) if x[0] != x[1])) == 1
    left = i - 1
    right = i
    repaired = False
    while left >= 0 and right < len(hashes):
        if hashes[left] != hashes[right]:
            if repaired:
                return False
            if is_smudge(hashes[left], hashes[right]):
                repaired = True
            else:
                return False
        left = left - 1
        right = right + 1
        if left < 0 or right > len(hashes) - 1:
            break
    return repaired

def get_reflection(hashes, is_reflection_func):
    for i in range(1, len(hashes)):
        if is_reflection_func(hashes, i):
            return i
        
    return None

def find_reflections(patterns, is_reflection_func):
    total = 0
    for pattern in patterns:
        columns = pattern.get_column_hashes()
        reflection = get_reflection(columns, is_reflection_func)
        if reflection is not None:
            total = total + reflection
            continue
        rows = pattern.get_row_hashes()
        reflection = get_reflection(rows, is_reflection_func)
        if reflection is not None:
            total = total + 100 * reflection
    return total

def main():
    patterns = parse('test.txt')
    assert find_reflections(patterns, is_reflection_pt1) == 405
    assert find_reflections(patterns, is_reflection_pt2) == 400
    patterns = parse('input.txt')
    print(find_reflections(patterns, is_reflection_pt1))
    print(find_reflections(patterns, is_reflection_pt2))
    pass

if __name__ == '__main__':
    main()
