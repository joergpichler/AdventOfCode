def parse(file):
    with open(file, 'r') as f:
        return list(map(lambda l: l.strip(), f.readlines()))

def getIllegalChar(line):
    stack = []
    for c in line:
        if(c == '(' or c == '[' or c == '{' or c == '<'):
            stack.append(c)
        else:
            pop = stack.pop()
            if(c == ')' and pop != '(' or c == ']' and pop != '[' or c == '}' and pop != '{' or c == '>' and pop != '<'):
                return (c, stack)
    
    return ('', stack)
            
def part1(lines):
    score = 0
    for line in lines:
        illegalChar = getIllegalChar(line)
        if(illegalChar[0] == ''):
            continue
        if(illegalChar[0] == ')'):
            score += 3
        elif(illegalChar[0] == ']'):
            score += 57
        elif(illegalChar[0] == '}'):
            score += 1197
        elif(illegalChar[0] == '>'):
            score += 25137
        else:
            raise Exception
    
    print(f'Pt1: {score}')

def part2(lines):
    scores = []
    
    for line in lines:
        result = getIllegalChar(line)
        if(result[0] != ''):
            continue
        stack = result[1]
        score = 0
        
        while(len(stack) > 0):
            element = stack.pop()
            score *= 5
            if(element == '('):
                score += 1
            elif(element == '['):
                score += 2
            elif(element == '{'):
                score += 3
            elif(element == '<'):
                score += 4
            else:
                raise Exception
            
        scores.append(score)
    
    scores.sort()
    middleScore = scores[int(len(scores) / 2)]
    print(f'Pt2: {middleScore}')

def main():
    lines = parse('input.txt')
    
    part1(lines)
    
    part2(lines)

if __name__ == '__main__':
    main()