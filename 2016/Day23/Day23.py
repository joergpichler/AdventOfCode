import re
from typing import List
from collections import defaultdict


class Machine:

    def __init__(self, init = None) -> None:
        self._vars = defaultdict(int)
        if init is not None:
            for k, v in init:
                self._vars[k] = v

    
    def _get_num(self, val):
        try:
            num = int(val)
        except ValueError:
            num = self._vars[val]
        return num


    def _toggle_instruction(self, index, instructions):
        if index >= len(instructions):
            return

        instruction = instructions[index].split(' ')
        if len(instruction) == 2:
            new_command = 'inc'
            if instruction[0] == 'inc':
                new_command = 'dec'
            instruction[0] = new_command
            instructions[index] = ' '.join(instruction)
            return
        elif len(instruction) == 3:
            new_command = 'jnz'
            if instruction[0] == 'jnz':
                new_command = 'cpy'
            instruction[0] = new_command
            instructions[index] = ' '.join(instruction)
            return

        raise Exception

    def run_instructions(self, instructions: List[str]):
        instruction_pointer = 0
        while instruction_pointer < len(instructions):
            instruction = instructions[instruction_pointer].split(' ')
            if instruction[0] == "cpy":
                target_var = instruction[2]
                if re.match(r'[a-z]', target_var):
                    try:
                        num = int(instruction[1])
                        self._vars[target_var] = num
                    except ValueError:
                        source_var = instruction[1]
                        self._vars[target_var] = self._vars[source_var]
                else:
                    print('invalid instruction {}'.format(instruction))
            elif instruction[0] == "inc":
                target_var = instruction[1]
                self._vars[target_var] += 1
            elif instruction[0] == "dec":
                target_var = instruction[1]
                self._vars[target_var] -= 1
            elif instruction[0] == "jnz":
                num = self._get_num(instruction[1])
                if num != 0:
                    jmp = self._get_num(instruction[2])
                    instruction_pointer += jmp
                    continue
            elif instruction[0] == 'tgl':
                num = self._get_num(instruction[1])
                self._toggle_instruction(instruction_pointer + num, instructions)
            else: 
                raise Exception

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
    assert m.get_var_value('a') == 3


def main():
    instructions = parse('input.txt')
    m = Machine([('a', 7)])
    m.run_instructions(instructions)
    a = m.get_var_value('a')
    print(f'Pt1: {a}')

    # takes a while to compute but works :)
    instructions = parse('input.txt')
    m = Machine([('a', 12)])
    m.run_instructions(instructions)
    a = m.get_var_value('a')
    print(f'Pt2: {a}')


if __name__ == '__main__':
    main()
    # test()
