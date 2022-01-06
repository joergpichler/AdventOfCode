from typing import List

class MyString:
    def __init__(self, s) -> None:
        self.s = s
        
    def __repr__(self) -> str:
        return self.s
    
    @property
    def len_characters_of_code(self):
        return len(self.s)
    
    @property
    def len_characters_of_string(self):
        s = eval(self.s)
        return len(s)
    
    @property
    def len_encoded_string(self):
        len = 2
        for c in self.s:
            if c == '"':
                len += 2
            elif c == '\\':
                len += 2
            else:
                len += 1
        return len

def parse(file):
    with open(file, 'r') as f:
        return [MyString(l.strip()) for l in f]

def run_assert_pt1(strings: List[MyString]):
    assert strings[0].len_characters_of_code == 2
    assert strings[0].len_characters_of_string == 0
    
    assert strings[1].len_characters_of_code == 5
    assert strings[1].len_characters_of_string == 3
    
    assert strings[2].len_characters_of_code == 10
    assert strings[2].len_characters_of_string == 7
    
    assert strings[3].len_characters_of_code == 6
    assert strings[3].len_characters_of_string == 1
    
    assert run_pt1(strings) == 12

def run_assert_pt2(strings: List[MyString]):
    assert strings[0].len_encoded_string == 6
    assert strings[1].len_encoded_string == 9
    assert strings[2].len_encoded_string == 16
    assert strings[3].len_encoded_string == 11
    
    assert run_pt2(strings) == 19

def run_pt1(strings: List[MyString]):
    total_characters_of_code = sum([s.len_characters_of_code for s in strings])
    total_characters_of_string = sum([s.len_characters_of_string for s in strings])
    return total_characters_of_code - total_characters_of_string

def run_pt2(strings: List[MyString]):
    total_characters_of_encoded_string = sum([s.len_encoded_string for s in strings])
    total_characters_of_code = sum([s.len_characters_of_code for s in strings])
    
    return total_characters_of_encoded_string - total_characters_of_code

def main():
    
    test_strings = parse('test.txt')
    
    run_assert_pt1(test_strings)
    
    strings = parse('input.txt')
    
    print(f'Pt1: {run_pt1(strings)}')
    
    run_assert_pt2(test_strings)
    
    print(f'Pt2: {run_pt2(strings)}')

if __name__ == '__main__':
    main()
