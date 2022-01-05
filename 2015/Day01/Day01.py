def getFloor(input: str, targetFloor: int = None):
    floor = 0
    for i in range(len(input)):
        c = input[i]
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1
        else:
            raise Exception
        if targetFloor is not None and floor == targetFloor:
            return i + 1
    return floor

def parse(input:str):
    with open(input, 'r') as f:
        return f.readline()

def main():
    assert getFloor('(())') == getFloor('()()') == 0
    assert getFloor('(((') == getFloor('(()(()(') == getFloor('))(((((') == 3
    assert getFloor('())') == getFloor('))(') == -1
    assert getFloor(')))') == getFloor(')())())') == -3
    
    input = parse('input.txt')
    print(f'Pt1: {getFloor(input)}')
    
    assert getFloor(')', -1) == 1
    assert getFloor('()())', -1) == 5
    
    print(f'Pt2: {getFloor(input, -1)}')

if __name__ == '__main__':
    main()
