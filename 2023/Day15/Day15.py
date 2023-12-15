def parse(file):
    with open(file, 'r') as f:
        line = f.readline().strip()
        return line.split(',')

def hash(text):
    value = 0
    for c in text:
        asc = ord(c)
        value += asc
        value *= 17
        value %= 256
    return value

def pt1(input):
    hashes = [hash(x) for x in input]
    return sum(hashes)

def debug_print(boxes):
    for i in range(len(boxes)):
        box = boxes[i]
        if len(box) == 0:
            continue
        print(f'Box {i}: ', end='')
        for lens in box:
            print(f'[{lens[0]} {lens[1]}] ', end='')
        print('')
    print()

def pt2(input):
    boxes = []
    for _ in range(256):
        boxes.append([])
    for instruction in input:
        if '=' in instruction:
            split = instruction.split('=')
            label = split[0]
            id = hash(label)
            focal = int(split[1])
            box = boxes[id]
            replaced = False
            for lens in box:
                if lens[0] == label:
                    lens[1] = focal
                    replaced = True
            if not replaced:
                box.append([label, focal])
        elif '-' in instruction:
            split = instruction.split('-')
            label = split[0]
            id = hash(label)
            box = boxes[id]
            remove_at = -1
            for i in range(len(box)):
                lens = box[i]
                if lens[0] == label:
                    remove_at = i
                    break
            if remove_at != - 1:
                del box[remove_at]
        #debug_print(boxes)
    total = 0
    for i in range(len(boxes)):
        box = boxes[i]
        for j in range(len(box)):
            focusing_power = (i + 1) * (j + 1) * box[j][1]
            total += focusing_power
    return total

def main():
    assert hash('HASH') == 52
    data = parse('test.txt')
    assert(pt1(data)) == 1320
    assert(pt2(data)) == 145
    data = parse('input.txt')
    print(pt1(data))
    print(pt2(data))

if __name__ == '__main__':
    main()
