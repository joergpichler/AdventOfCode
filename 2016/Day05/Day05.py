def calculate_hash(text: str):
    import hashlib
    hash = hashlib.md5(text.encode())
    return hash.hexdigest()

def get_next_hash(prefix, start_number):
    target = '0' * 5
    
    while True:
        text = f'{prefix}{start_number}'
        hash = calculate_hash(text)
        
        if hash[:5] == target:
            break
        
        start_number += 1
        
    return (hash, start_number)

def calculate_password_v1(prefix):
    password = ''
    number = 0
    
    for _ in range(8):
        (hash, number) = get_next_hash(prefix, number)
        password += hash[5]
        number += 1
        
    return password

def calculate_password_v2(id):
    password = {}
    number = 0
    
    while len(password) < 8:
        (hash, number) = get_next_hash(id, number)
        number += 1
        try:
            position_in_password = int(hash[5])
        except ValueError:
            continue
        character = hash[6]
        if position_in_password < 8 and position_in_password not in password:
            password[position_in_password] = character
            
    result = ''
    for i in range(8):
        result += password[i]
        
    return result
    
def main():
    prefix = 'abc'
    assert calculate_password_v1(prefix) == '18f47a30'
    assert calculate_password_v2(prefix) == '05ace8e3'
    
    prefix = 'wtnhxymk'
    
    password = calculate_password_v1(prefix)
    print(f'Pt1: {password}')

    password = calculate_password_v2(prefix)
    print(f'Pt2: {password}')

if __name__ == '__main__':
    main()
