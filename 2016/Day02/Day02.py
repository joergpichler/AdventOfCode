from typing import Tuple
import numpy as np
from abc import ABC, abstractmethod

class InputPad(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.pad, self.start_coord = self.init_pad()

    @abstractmethod
    def init_pad(self) -> Tuple:
        pass

    @abstractmethod
    def can_move_to(self, coord) -> bool:
        pass

    @abstractmethod
    def get_at(self, coord) -> str:
        pass

    def enter(self, input):
        coord = self.start_coord
        numstr = ""
        for instr in input:
            for c in instr:
                if c == 'U':
                    next_coord = (coord[0] - 1, coord[1])
                elif c == 'L':
                    next_coord = (coord[0], coord[1] - 1)
                elif c == 'R':
                    next_coord = (coord[0], coord[1] + 1)
                elif c == 'D':
                    next_coord = (coord[0] + 1, coord[1])
                if self.can_move_to(next_coord):
                    coord = next_coord
            numstr += self.get_at(coord)

        return numstr

class Numpad(InputPad):

    def init_pad(self):
        pad = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        return (pad, (1,1))

    def can_move_to(self, coord):
        if coord[0] < 0 or coord[1] < 0:
            return False
        return coord[0] < self.pad.shape[0] and coord[1] < self.pad.shape[1]

    def get_at(self, coord):
        return str(self.pad[coord])

class BathroomPad(InputPad):

    def init_pad(self):
        pad = {
            (0,2): "1",
            (1,1): "2", (1,2): "3", (1,3): "4",
            (2,0): "5", (2,1): "6", (2,2): "7", (2,3): "8", (2,4): "9",
            (3,1): "A", (3,2): "B", (3,3): "C",
            (4,2): "D",
        }
        return (pad, (2,0))
    
    def can_move_to(self, coord):
        return coord in self.pad

    def get_at(self, coord):
        return self.pad[coord]

def parse(file):
    with open(file, 'r') as f:
        return [l.strip() for l in f]

def main():
    test = parse('test.txt')
    input = parse('input.txt')

    numpad = Numpad()
    assert numpad.enter(test) == "1985"
    bathroom_pad = BathroomPad()
    assert bathroom_pad.enter(test) == "5DB3"
    
    print(f'Pt1: {numpad.enter(input)}')
    print(f'Pt2: {bathroom_pad.enter(input)}')

if __name__ == '__main__':
    main()
