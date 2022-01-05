import re

class Instruction:
    def __init__(self, inst, opA, opB) -> None:
        self.operation = inst
        self.opA = opA
        self.opB = opB
        pass
    
    def __repr__(self) -> str:
        str = f'{self.operation} {self.opA}'
        if self.opB is not None:
            str += f' {self.opB}'
        return str
    
def parse(file):
    instructions = []
    with open(file, 'r') as f:
        for line in f:
            split = line.strip().split(' ')
            instructions.append(Instruction(split[0], split[1], split[2] if len(split) == 3 else None))
    return instructions
    
def to_py(instructions):
    out = ["w = x = y = z = 0\n", "i = 0\n", "input = list(map(int, num))\n"]
    
    for instruction in instructions:
            
        if instruction.operation == 'inp':
            instr = f"{instruction.opA} = input[i]\ni += 1"
        elif instruction.operation == 'add':
            instr = f"{instruction.opA} = {instruction.opA} + {instruction.opB}"
        elif instruction.operation == 'mul':
            instr = f"{instruction.opA} = {instruction.opA} * {instruction.opB}"
        elif instruction.operation == 'div':
            instr = f"{instruction.opA} = int({instruction.opA} / {instruction.opB})"
        elif instruction.operation == 'mod':
            instr = f"{instruction.opA} = {instruction.opA} % {instruction.opB}"
        elif instruction.operation == 'eql':
            instr = f"{instruction.opA} = 1 if {instruction.opA} == {instruction.opB} else 0"
        else:
            raise Exception
        out.append(instr + "\n")
        
    with open('C:/temp/temp.py', 'w') as f:
        f.writelines(out)

def main():
    instructions = parse('input.txt')
    to_py(instructions)
    

if __name__ == '__main__':
    main()
