import re
from collections import deque
from typing import List
from itertools import permutations
from abc import ABC, abstractmethod

class Instruction(ABC):
    @abstractmethod
    def apply(self, str: List[str]) -> List[str]:
        pass

    @abstractmethod
    def invert(self, str: List[str]) -> List[str]:
        pass

class SwapPositionInstruction(Instruction):
    def __init__(self, pos_a: int, pos_b: int) -> None:
        self.pos_a = pos_a
        self.pos_b = pos_b

    def apply(self, str: List[str]) -> List[str]:
        a = str[self.pos_a]
        str[self.pos_a] = str[self.pos_b]
        str[self.pos_b] = a
        return str

    def invert(self, str: List[str]) -> List[str]:
        '''Swapping a and b is the same as swapping b and a'''
        return self.apply(str)

class SwapLetterInstruction(Instruction):
    def __init__(self, letter_a, letter_b) -> None:
        self.letter_a = letter_a
        self.letter_b = letter_b

    def apply(self, str) -> str:
        indices_a = [i for i, x in enumerate(str) if x == self.letter_a]
        indices_b = [i for i, x in enumerate(str) if x == self.letter_b]
        for i in indices_a:
            str[i] = self.letter_b
        for i in indices_b:
            str[i] = self.letter_a
        return str

    def invert(self, str: List[str]) -> List[str]:
        return self.apply(str)

class ReversePositionsInstruction(Instruction):
    def __init__(self, pos_a: int, pos_b: int) -> None:
        self.pos_a = pos_a
        self.pos_b = pos_b

    def apply(self, str: List[str]) -> List[str]:
        str = str[0:self.pos_a] + list(reversed(str[self.pos_a:self.pos_b+1])) + str[self.pos_b+1:len(str)]
        return str

    def invert(self, str: List[str]) -> List[str]:
        return self.apply(str)

class MovePositionInstruction(Instruction):
    def __init__(self, pos_a: int, pos_b: int) -> None:
        self.pos_a = pos_a
        self.pos_b = pos_b

    @staticmethod
    def _apply(str: List[str], pos_a: int, pos_b: int) -> List[str]:
        c = str.pop(pos_a)
        str.insert(pos_b, c)
        return str

    def apply(self, str: List[str]) -> List[str]:
        return MovePositionInstruction._apply(str, self.pos_a, self.pos_b)

    def invert(self, str: List[str]) -> List[str]:
        return MovePositionInstruction._apply(str, self.pos_b, self.pos_a)

def rotate(str: List, n: int) -> List:
    '''Positive values are right rotations'''
    d = deque(str)
    d.rotate(n)
    return list(d)

class RotateInstruction(Instruction):
    def __init__(self, n: int):
        self.n = n

    def apply(self, str: List[str]) -> List[str]:
        return rotate(str, self.n)

    def invert(self, str: List[str]) -> List[str]:
        return rotate(str, -self.n)

class RotateCharacterInstruction(Instruction):
    def __init__(self, c: str) -> None:
        self.c = c

    def _get_rotation(self, str: List[str]):
        if self.c != '':
            
            rotation %= len(str)
            return rotation if not self.left else -rotation
        return self.n if not self.left else -self.n

    def apply(self, str):
        index = str.index(self.c)
        rotation = index + 1
        if index >= 4:
            rotation += 1
        return rotate(str, rotation)

    def invert(self, str: List[str]) -> List[str]:
        if len(str) == 8:
            index = str.index(self.c)
            match index:
                case 0:
                    return rotate(str, -1)
                case 1:
                    return rotate(str, -1)
                case 2:
                    return rotate(str, 2)
                case 3:
                    return rotate(str, -2)
                case 4:
                    return rotate(str, 1)
                case 5:
                    return rotate(str, -3)
                case 6:
                    return str
                case 7:
                    return rotate(str, -4)

            raise Exception
        raise Exception

class InstructionFactory:
    def create_instruction(self, instruction_string: str):
        match = re.match(r'^swap position (\d+).*(\d+)$', instruction_string)
        if match:
            return SwapPositionInstruction(int(match.group(1)), int(match.group(2)))
        match = re.match(r'^swap letter ([a-z]).*([a-z])$', instruction_string)
        if match:
            return SwapLetterInstruction(match.group(1), match.group(2))
        match = re.match(r'^reverse positions (\d+).*(\d+)$', instruction_string)
        if match:
            return ReversePositionsInstruction(int(match.group(1)), int(match.group(2)))
        match = re.match(r'^rotate (left|right) (\d+).*$', instruction_string)
        if match:
            sign = -1 if match.group(1) == 'left' else 1
            return RotateInstruction(sign * int(match.group(2)))
        match = re.match(r'^move position (\d+).*(\d+)$', instruction_string)
        if match:
            return MovePositionInstruction(int(match.group(1)), int(match.group(2)))
        match = re.match(r'^rotate based on position of letter ([a-z])$', instruction_string)
        if match:
            return RotateCharacterInstruction(match.group(1))
        raise Exception

def parse(file):
    factory = InstructionFactory()
    with open(file, 'r') as f:
        return [factory.create_instruction(l.strip()) for l in f]

def apply_instructions(input: str, instructions: List[Instruction], invert = False) -> str:
    input = list(input)
    for instr in (instructions if not invert else reversed(instructions)):
        input = instr.apply(input) if not invert else instr.invert(input)
    return "".join(input)

def main():
    test_instructions = parse('test.txt')

    result = apply_instructions('abcde', test_instructions)
    assert result == "decab"

    instructions = parse('input.txt')

    result = apply_instructions('abcdefgh', instructions)
    print(f'Pt1: {result}')

    result = apply_instructions('fbgdceah', instructions, True)
    print(f'Pt2: {result}')

    # brute force alternative

    l = list('fbgdceah')
    l.sort()
    for p in permutations(l):
        result = apply_instructions(p, instructions)
        if result == 'fbgdceah':
            print('Pt2 - alt: {}'.format(''.join(p)))

if __name__ == '__main__':
    main()
