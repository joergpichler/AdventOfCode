import hashlib

def hash(id, num):
    str = f'{id}{num}'
    hash = hashlib.md5(str.encode())
    return hash.hexdigest()

def get_next(id, num):
    target = ''.zfill(5)
    hashed = hash(id, num)
    while hashed[:5] != target:
        num += 1
        hashed = hash(id, num)
    return (hashed, num)

def get_pw(id):
    pw = ''
    num = 0
    for _ in range(8):
        (hash, num) = get_next(id, num)
        pw += hash[5]
        num += 1
    return pw

def get_pw_2(id):
    pw = {}
    num = 0
    while len(pw) < 8:
        (hash, num) = get_next(id, num)
        num += 1
        try:
            pos = int(hash[5])
        except ValueError:
            continue
        character = hash[6]
        if pos < 8 and pos not in pw:
            pw[pos] = character
            #print(f'{pos} = {character}')
    result = ''
    for i in range(8):
        result += pw[i]
    return result
    
def main():
    id = 'abc'
    assert get_pw(id) == '18f47a30'
    assert get_pw_2(id) == '05ace8e3'
    
    id = 'wtnhxymk'
    
    pw = get_pw(id)
    print(f'Pt1: {pw}')

    pw = get_pw_2(id)
    print(f'Pt2: {pw}')

if __name__ == '__main__':
    main()
