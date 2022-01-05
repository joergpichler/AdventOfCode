import hashlib

def findNumber(secretKey: str, minNumZeroes = 5):
    targetStr = ''.zfill(minNumZeroes)
    found = False
    num = 0
    while not found:
        num += 1
        str = f'{secretKey}{num}'
        hash = hashlib.md5(str.encode())
        if hash.hexdigest()[:minNumZeroes] == targetStr:
            found = True
    return num

def main():
    assert findNumber('abcdef') == 609043
    assert findNumber('pqrstuv') == 1048970
    print('Pt1: {}'.format(findNumber('iwrupvqb')))
    print('Pt2: {}'.format(findNumber('iwrupvqb', 6)))

if __name__ == '__main__':
    main()
