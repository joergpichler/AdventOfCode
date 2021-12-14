import re

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

def ensureDictEntry(key, dict):
    if not key in dict:
        dict[key] = 0

def calcPolymer(input, rules, steps):
    pairs = {}
    chars = {}
    for i in range(len(input)- 1):
        pair = input[i:i+2]
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1
    for i in range(len(input)):
        char = input[i]
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1
            
    for i in range(steps):
        for pair, v in pairs.copy().items():
            rule = rules[pair]
            
            pairs[pair] -= v
            
            key = pair[0] + rule
            ensureDictEntry(key, pairs)
            pairs[key] += v
            
            key = rule + pair[1]
            ensureDictEntry(key, pairs)
            pairs[key] += v
            
            ensureDictEntry(rule, chars)
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