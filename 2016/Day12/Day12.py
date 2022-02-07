from typing import Iterable
from collections import defaultdict


class Machine:

    def __init__(self, init = None) -> None:
        self._vars = defaultdict(int)
        if init is not None:
            for k, v in init:
                self._vars[k] = v


    def run_instructions(self, instructions: Iterable[str]):
        instruction_pointer = 0
        while instruction_pointer < len(instructions):
            instruction = instructions[instruction_pointer].split(' ')
            if instruction[0] == "cpy":
                target_var = instruction[2]
                try:
                    num = int(instruction[1])
                    self._vars[target_var] = num
                except ValueError:
                    source_var = instruction[1]
                    self._vars[target_var] = self._vars[source_var]
            elif instruction[0] == "inc":
                target_var = instruction[1]
                self._vars[target_var] += 1
            elif instruction[0] == "dec":
                target_var = instruction[1]
                self._vars[target_var] -= 1
            elif instruction[0] == "jnz":
                try:
                    num = int(instruction[1])
                except ValueError:
                    num = self._vars[instruction[1]]

                if num != 0:
                    instruction_pointer += int(instruction[2])
                    continue

            instruction_pointer += 1
        pass


    def get_var_value(self, name):
        return self._vars[name]


def parse(file):
    with open(file, 'r') as f:
        return [l.strip() for l in f]


def test():
    instructions = parse('test.txt')
    m = Machine()
    m.run_instructions(instructions)
    assert m.get_var_value('a') == 42


def main():
    instructions = parse('input.txt')
    m = Machine()
    #m.run_instructions(instructions)
    a = m.get_var_value('a')
    print(f'Pt1: {a}')

    m = Machine([('c', 1)])
    m.run_instructions(instructions)
    a = m.get_var_value('a')
    print(f'Pt2: {a}')


if __name__ == '__main__':
    main()
