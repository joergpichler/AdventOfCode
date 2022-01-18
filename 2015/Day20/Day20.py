import math

def divisor_generator(n):
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                yield int(n / i)
                
def divisor_generator_2(n):
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            if i * 50 >= n:
                yield i
            if i*i != n:
                divi = int(n / i)
                if divi * 50 >= n:
                    yield divi
        
def get_house_score(num):
    return sum([x * 10 for x in divisor_generator(num)])

def get_house_score_2(num):
    return sum([x * 11 for x in divisor_generator_2(num)])
                
def main():
    
    assert get_house_score(1) == 10
    assert get_house_score(2) == 30
    assert get_house_score(3) == 40
    assert get_house_score(4) == 70
    assert get_house_score(5) == 60
    assert get_house_score(6) == 120
    assert get_house_score(7) == 80
    assert get_house_score(8) == 150
    assert get_house_score(9) == 130

    num = 1
    while True:
        if get_house_score(num) >= 29000000:
            break
        num +=1

    print(f'Pt1: {num}')
    
    num = 1
    while True:
        if get_house_score_2(num) >= 29000000:
            break
        num +=1
    
    print(f'Pt2: {num}')

if __name__ == '__main__':
    main()
