def validate(pwd:str):
    if not len(pwd) == 8:
        return False
    
    if 'i' in pwd or 'o' in pwd or 'l' in pwd:
        return False
    
    has_increasing = False
    pairs = [False, False]
    skipPairs = False
    
    for i in range(len(pwd) - 1):
        if not skipPairs:
            if pwd[i] == pwd[i+1]:
                if not pairs[0]:
                    pairs[0] = True
                    skipPairs = True
                elif not pairs[1]:
                    pairs[1] = True
                    skipPairs = True
        else:
            skipPairs = False
            
        if i < len(pwd) -2 and ord(pwd[i]) == ord(pwd[i+1]) - 1 == ord(pwd[i+2]) - 2:
            has_increasing = True
    
    return has_increasing and pairs[0] and pairs[1]

def get_next_char(c:str):
    idx = ord(c) - 97 #97 is idx of a
    idx += 1
    overflow = idx == 26
    idx = idx % 26
    return (chr(idx + 97), overflow)

def get_next_pwd(pwd:str):
    arr = [c for c in pwd]
    overflow = True
    idx = 0
    while overflow:
        idx -= 1
        c, overflow = get_next_char(arr[idx])
        arr[idx] = c
    return "".join(arr)

def get_next_valid_pwd(pwd:str):
    next_pwd = get_next_pwd(pwd)
    while not validate(next_pwd):
        next_pwd = get_next_pwd(next_pwd)
    return next_pwd

def test():
    abc = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(abc) - 1):
        assert get_next_char(abc[i])[0] == abc[i+1]
        assert get_next_char(abc[i])[1] == False
    assert get_next_char(abc[-1])[0] == abc[0]
    assert get_next_char(abc[-1])[1] == True
    
    assert validate('hijklmmn') == False
    assert validate('abbceffg') == False
    assert validate('abbcegjk') == False
    
    assert get_next_valid_pwd('abcdefgh') == 'abcdffaa'
    assert get_next_valid_pwd('ghijklmn') == 'ghjaabcc'

def main():
    test()
    
    pt1 = get_next_valid_pwd('hxbxwxba')
    print(f'Pt1: {pt1}')
    
    pt2 = get_next_valid_pwd(pt1)
    print(f'Pt2: {pt2}')

if __name__ == '__main__':
    main()
