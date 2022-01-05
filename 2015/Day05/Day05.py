import numpy as np

def parse(file):
    with open(file, 'r') as f:
        return [l.strip() for l in f]

def isNice(s: str):
    vowelCount = 0
    for v in 'aeiou':
        vowelCount += s.count(v)
    
    if vowelCount < 3:
        return False
    
    containsLetterTwiceInRow = False
    
    for i in range(len(s) - 1):
        c = s[i]
        n = s[i + 1]
        if c == n:
            containsLetterTwiceInRow = True
    
    if not containsLetterTwiceInRow:
        return False
    
    invalidStrings = ['ab', 'cd', 'pq', 'xy']
    for invalidString in invalidStrings:
        if invalidString in s:
            return False
    
    return True

def isNice2(s: str):
    pairAppearsTwice = False
    
    for i in range(len(s) - 2):
        pair = s[i:i+2]
        if s.count(pair) >= 2:
            pairAppearsTwice = True
            break
    
    if not pairAppearsTwice:
        return False
    
    hasRepeatingLetter = False
    
    for i in range(len(s) - 2):
        if s[i] == s[i+2]:
            hasRepeatingLetter = True
            break
    
    return hasRepeatingLetter

def main():
    assert isNice('ugknbfddgicrmopn')
    assert isNice('aaa')
    assert isNice('jchzalrnumimnmhp') == False
    assert isNice('haegwjzuvuyypxyu') == False
    assert isNice('dvszwmarrgswjxmb') == False
    
    strings = parse('input.txt')
    
    print(f'Pt1: {sum(map(lambda x: isNice(x), strings))}')
    
    assert isNice2('qjhvhtzxzqqjkmpb')
    assert isNice2('xxyxx')
    assert isNice2('uurcxstgmygtbstg') == False
    assert isNice2('ieodomkazucvgmuy') == False
    
    print(f'Pt2: {sum(map(lambda x: isNice2(x), strings))}')

if __name__ == '__main__':
    main()
