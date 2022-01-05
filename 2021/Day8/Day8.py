import numpy as np

def parseInput(file):
    with open(file, 'r') as f:
        return [list(map(lambda x: x.split(' '), line.strip().split(' | '))) for line in f]

def part1(displays):
    sum = 0
    for display in displays:
        countInOut = np.array(list(map(len, display[1])))
        target = np.where((countInOut == 2) | (countInOut == 4) | (countInOut == 3) | (countInOut == 7))[0]
        sum += target.size
    
    print(f"Part 1: Sum {sum}")

def eliminate(number, wires, numbersToSegements, segmentsToWires):
    segments = numbersToSegements[number]
    for i in range(7):
        possibleWiresInSegement = segmentsToWires[i]
        # if the segment is in the digit remove all other wires
        if i in segments:
            toRemove = [x for x in possibleWiresInSegement if not x in wires]
            for r in toRemove:
                possibleWiresInSegement.remove(r)
        # if the segment is not in the digit, remove the wires from the digit
        else:
            for c in wires:
                if c in possibleWiresInSegement:
                    possibleWiresInSegement.remove(c)
        
def sortCharsInStr(s):
    sortedChars = sorted(s)
    return ''.join(sortedChars)

def determineSegments(display):
    numbersToSegements = {0: [0, 1, 2, 4, 5, 6],
                          1: [2, 5],
                          2: [1, 2, 3, 4, 6],
                          3: [1, 2, 3, 5, 6],
                          4: [0, 2, 3, 5],
                          5: [0, 1, 3, 5, 6],
                          6: [0, 1, 3, 4, 5, 6],
                          7: [1, 2, 5],
                          8: [0, 1, 2, 3, 4, 5, 6],
                          9: [0, 1, 2, 3, 5, 6]}
    segmentsToWires = {0 : ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                       1: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                       2: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                       3: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                       4: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                       5: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                       6: ['a', 'b', 'c', 'd', 'e', 'f', 'g']}
    dict = {}
    digits = display[0]
    digitsCount = np.array([len(i) for i in digits])
    
    # 8
    idx8 = np.where(digitsCount == 7)[0][0]
    dict[8] = digits[idx8]
    eliminate(8, dict[8], numbersToSegements, segmentsToWires)
    # 1
    idx1 = np.where(digitsCount == 2)[0][0]
    dict[1] = digits[idx1]
    eliminate(1, dict[1], numbersToSegements, segmentsToWires)
    # 4
    idx4 = np.where(digitsCount == 4)[0][0]
    dict[4] = digits[idx4]
    eliminate(4, dict[4], numbersToSegements, segmentsToWires)
    # 7
    idx7 = np.where(digitsCount == 3)[0][0]
    dict[7] = digits[idx7]
    eliminate(7, dict[7], numbersToSegements, segmentsToWires)
    
    digits.remove(dict[8])
    digits.remove(dict[1])
    digits.remove(dict[4])
    digits.remove(dict[7])
    
    #find out which of segment 6 is in all --> segment 6 & 4 determined
    possibilities = segmentsToWires[6]
    segment6 = ''
    if sum([1 for x in digits if possibilities[0] in x]) == 6:
        segment6 = possibilities[0]
    else:
        segment6 = possibilities[1]
    
    segmentsToWires[4].remove(segment6)
    segmentsToWires[6] = [segment6]
    
    # one of segment 3 is in all but 1
    possibilities = segmentsToWires[0]
    segment3 = ''
    if sum([1 for x in digits if possibilities[0] in x]) == 5:
        segment3 = possibilities[0]
    else:
        segment3 = possibilities[1]
    
    segmentsToWires[0].remove(segment3)
    segmentsToWires[3] = [segment3]
    
    # one of segment 2 is in 4
    possibilities = segmentsToWires[2]
    segment2 = ''
    if sum([1 for x in digits if possibilities[0] in x]) == 4:
        segment2 = possibilities[0]
    else:
        segment2 = possibilities[1]
    
    segmentsToWires[5].remove(segment2)
    segmentsToWires[2] = [segment2]
    
    # missing numbers
    for n in [0, 2, 3, 5, 6, 9]:
        chars = ''
        segments = numbersToSegements[n]
        for s in segments:
            chars += segmentsToWires[s][0]
        dict[n] = sortCharsInStr(chars)
    
    # sort remaining entries
    dict[8] = sortCharsInStr(dict[8])
    dict[1] = sortCharsInStr(dict[1])
    dict[4] = sortCharsInStr(dict[4])
    dict[7] = sortCharsInStr(dict[7])
    
    # reverse the dictionary#
    dict = {v: k for k, v in dict.items()}
    
    result = ''
    for toDecode in display[1]:
        result += str(dict[sortCharsInStr(toDecode)])
    
    return int(result)

def part2(displays):
    sum = 0
    for display in displays:
        sum += determineSegments(display)
    
    print(f'Part 2: {sum}')

def main():
    displays = parseInput('input.txt')
    
    part1(displays)
    part2(displays)

if __name__ == '__main__':
    main()