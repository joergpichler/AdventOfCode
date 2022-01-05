def parse(file):
    with open(file, 'r') as f:
        return list(map(lambda x: list(map(int, x.strip().split('x'))), f))

def calcPaperArea(l, w, h):
    area = 2 * l * w + 2 * w * h + 2 * h * l
    minSide = min([l * w, w * h, h * l])
    return area + minSide

def calcRibbon(l, w, h):
    sorted = [l, w, h]
    sorted.sort()
    return sorted[0] * 2 + sorted[1] * 2 + (l*w*h)

def main():
    assert calcPaperArea(2,3,4) == 58
    assert calcPaperArea(1,1,10) == 43
    
    boxes = parse('input.txt')
    sizes = list(map(lambda x: calcPaperArea(x[0], x[1], x[2]), boxes))
    print(f'Pt1: {sum(sizes)}')
    
    assert calcRibbon(2,3,4) == 34
    assert calcRibbon(1,1,10) == 14
    
    ribbons = list(map(lambda x: calcRibbon(x[0], x[1], x[2]), boxes))
    print(f'Pt2: {sum(ribbons)}')

if __name__ == '__main__':
    main()
