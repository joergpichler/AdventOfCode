import numpy as np

class naive_cycle_detector:
    def __init__(self, seq, min_cycle_len = 4) -> None:
        self.seq = seq
        self.min_cycle_len = min_cycle_len

    def _detect_cycle(self, values):
        cycle_len = self.min_cycle_len

        while len(values) >= 2 * cycle_len:
            last_elems = values[-cycle_len:]
            elems = values[-2*cycle_len:-cycle_len]
            
            if last_elems == elems:
                return len(values) - 2 * cycle_len, cycle_len
            
            cycle_len += 1
            
        return None, None

    def detect_cycle(self):
        self.values = []
        
        for _ in range(self.min_cycle_len * 2 - 1):
            self.values.append(next(self.seq))
        
        for _ in range(100000):
            self.values.append(next(self.seq))

            cycle_start, cycle_length = self._detect_cycle(self.values)
            if cycle_start is not None:
                self.cycle_start = cycle_start
                self.cycle_length = cycle_length
                return cycle_start, cycle_length

        raise Exception
    
    def get_element_at(self, p):
        k = (p - self.cycle_start) % self.cycle_length
        value = self.values[k + self.cycle_start - 1]
        return value
        
def parse(file):
    with open(file, 'r') as f:
        return np.array([list(x.strip()) for x in f])

def move_rocks(data):
    rocks_moved = False
    for i_row in range(data.shape[0] - 1): # skip last row
        for i_col in range(data.shape[1]):
            val = data[i_row, i_col]
            if val == '.' and data[i_row + 1, i_col] == 'O':
                rocks_moved = True
                data[i_row, i_col] = 'O'
                data[i_row + 1, i_col] = '.'

    return rocks_moved

def tilt(data, direction):
    match direction:
        case 'W':
            data = np.rot90(data, 3)
        case 'S':
            data = np.rot90(data, 2)
        case 'E':
            data = np.rot90(data, 1)
        case _:
            pass

    while(move_rocks(data)):
        pass

    match direction:
        case 'W':
            data = np.rot90(data, 1)
        case 'S':
            data = np.rot90(data, 2)
        case 'E':
            data = np.rot90(data, 3)
        case _:
            pass

    return data

def calc_load(data):
    load = 0
    for i in range(data.shape[0] - 1, -1, -1):
        value = data.shape[0] - i
        load = load + (sum((1 for x in data[i, :] if x == 'O')) * value)
    return load

def pt1(data):
    data = tilt(data, 'N')
    return calc_load(data)

def enumerate_results(data):
    while True:
        data = tilt(data, 'N')
        data = tilt(data, 'W')
        data = tilt(data, 'S')
        data = tilt(data, 'E')
        yield calc_load(data)

def pt2(data):
    detector = naive_cycle_detector(enumerate_results(data))
    cycle_start, _ = detector.detect_cycle()
    if cycle_start is not None:
        return detector.get_element_at(1000000000)
    pass

def main():
    data = parse('test.txt')
    assert pt1(data) == 136
    data = parse('test.txt')
    assert pt2(data) == 64
    data = parse('input.txt')
    print(pt1(data))
    data = parse('input.txt')
    print(pt2(data))

if __name__ == '__main__':
    main()
