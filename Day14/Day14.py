import re
from collections import defaultdict

def parse(file):
    input = ''
    rules = {}
    with open(file, 'r') as f:
        input = f.readline().strip()
        f.readline()
        for line in f:
            match = re.match(r"([A-Z]+)\s->\s([A-Z])", line)
            rules[match.group(1)] = match.group(2)
    return (input, rules)

def calcPolymer(input, rules, steps):
    pairs = defaultdict(int)
    chars = defaultdict(int)
    
    for i in range(len(input)- 1):
        pair = input[i:i+2]
        pairs[pair] += 1
    for i in range(len(input)):
        char = input[i]
        chars[char] += 1
            
    for i in range(steps):
        for pair, v in pairs.copy().items():
            rule = rules[pair]
            
            pairs[pair] -= v
            
            key = pair[0] + rule
            pairs[key] += v
            
            key = rule + pair[1]
            pairs[key] += v
            
            chars[rule] += v
    
    maxKey = max(chars, key=lambda key: chars[key])
    minKey = min(chars, key=lambda key: chars[key])
    
    print(f'{chars[maxKey] - chars[minKey]}')
    
def main():
    input, rules = parse('input.txt')
    
    calcPolymer(input, rules, 10)
    calcPolymer(input, rules, 40)

if __name__ == '__main__':
    main()