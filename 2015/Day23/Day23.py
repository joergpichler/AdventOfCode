from typing import List
from collections import defaultdict

class Instruction:
    def __init__(self, l: str) -> None:
        split = l.split(' ', 1)
        self.command = split[0]
        self.variable = None
        self.num = None
        if(self.command == 'jio' or self.command == 'jie'):
            split = split[-1].split(', ')
            self.variable = split[0]
            self.num = int(split[-1].strip())
        elif self.command == 'jmp':
            self.num = int(split[-1].strip())
        else:
            self.variable = split[-1].strip()

    def __repr__(self) -> str:
        return f'{self.command} {self.variable} {self.num}'

class Machine:
    def __init__(self) -> None:
        self.instruction_ptr = 0
        self.variables = defaultdict(int)

    def run(self, instructions: List[Instruction]):
        while self.instruction_ptr >= 0 and self.instruction_ptr < len(instructions):
            instruction = instructions[self.instruction_ptr]
            if instruction.command == 'hlf':
                self.variables[instruction.variable] /= 2
                self.instruction_ptr += 1
            elif instruction.command == 'tpl':
                self.variables[instruction.variable] *= 3
                self.instruction_ptr += 1
            elif instruction.command == 'inc':
                self.variables[instruction.variable] += 1
                self.instruction_ptr += 1
            elif instruction.command == 'jmp':
                self.instruction_ptr += instruction.num
            elif instruction.command == 'jie':
                if self.variables[instruction.variable] % 2 == 0:
                    self.instruction_ptr += instruction.num
                else:
                    self.instruction_ptr += 1
            elif instruction.command == 'jio':
                if self.variables[instruction.variable] == 1:
                    self.instruction_ptr += instruction.num
                else:
                    self.instruction_ptr += 1
            else:
                raise Exception()

def parse(file):
    with open(file, 'r') as f:
        return [Instruction(l) for l in f]

def main():
    instructions = parse('input.txt')
    machine = Machine()
    machine.run(instructions)

    result = machine.variables['b']
    print(f'Pt1: {result}')

    machine = Machine()
    machine.variables['a'] = 1
    machine.run(instructions)

    result = machine.variables['b']
    print(f'Pt2: {result}')

if __name__ == '__main__':
    main()
