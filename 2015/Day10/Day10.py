def look_and_say(input: str):
    result = ''
    idx = 0
    while idx < len(input):
        num = int(input[idx])
        count = 0
        while idx < len(input) and int(input[idx]) == num:
            count += 1
            idx += 1
            
        result += f'{count}{num}'
    
    return result
    

def main():
    assert look_and_say('1') == '11'
    assert look_and_say('11') == '21'
    assert look_and_say('21') == '1211'
    assert look_and_say('1211') == '111221'
    assert look_and_say('111221') == '312211'
    
    input = "1321131112"
    
    tmp = input
    for _ in range(40):
        tmp = look_and_say(tmp)
        
    print(f'Pt1: {len(tmp)}')
    
    for _ in range(10):
        tmp = look_and_say(tmp)
        
    print(f'Pt2: {len(tmp)}')
    
    pass

if __name__ == '__main__':
    main()
