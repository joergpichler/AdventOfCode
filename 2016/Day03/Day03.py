class Triangle:
    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c
        
    @property
    def is_valid(self):
        ab = self.a + self.b
        ac = self.a + self.c
        bc = self.b + self.c
        return ab > self.c and ac > self.b and bc > self.a

def parse(file):
    import re
    with open(file, 'r') as f:
        for l in f:
            match = re.findall('\d+', l)
            yield Triangle(int(match[0]), int(match[1]), int(match[2]))

def parse_alt(file):
    import numpy as np
    arr = np.loadtxt(file, dtype=np.int32)
    numbers = list(arr[:,0]) + list(arr[:,1]) + list(arr[:,2])
    assert len(numbers) % 3 == 0
    for i in range(0, len(numbers), 3):
        yield Triangle(numbers[i], numbers[i+1], numbers[i+2])

def main():
    assert Triangle(5, 10, 25).is_valid == False
    
    triangles = list(parse('input.txt'))
    valid_triangles = sum(t.is_valid for t in triangles)
    print(f'Pt1: {valid_triangles}')
    
    triangles = list(parse_alt('input.txt'))
    valid_triangles = sum(t.is_valid for t in triangles)
    print(f'Pt2: {valid_triangles}')

if __name__ == '__main__':
    main()
