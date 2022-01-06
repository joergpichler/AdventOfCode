import re
import numpy as np

class Instruction:
    def __init__(self, s: str) -> None:
        match = re.match(r'^(.+?)\s->\s(\w+)$', s)
        self.do = match.group(1)
        self.variable = match.group(2)
        
    def __repr__(self) -> str:
        return f'{self.variable} = {self.do}'

class Machine:
    def __init__(self) -> None:
        self.cache = {}
        pass
    
    def reset(self) -> None:
        self.cache.clear()
    
    def get_value(self, variable, instructions: dict):

        if re.match(r'^\d+$', variable):
            return np.uint16(variable)
        
        if variable in self.cache:
            return self.cache[variable]
        
        instruction = instructions[variable]
        
        numberOnlyMatch = re.match(r'^\d+$', instruction.do)
        if numberOnlyMatch:
            result = np.uint16(numberOnlyMatch.group(0))
        elif 'AND' in instruction.do:
            split = instruction.do.split('AND')
            var_a = split[0].strip()
            var_b = split[1].strip()
            result =  self.get_value(var_a, instructions) & self.get_value(var_b, instructions)
        elif 'OR' in instruction.do:
            split = instruction.do.split('OR')
            var_a = split[0].strip()
            var_b = split[1].strip()
            result = self.get_value(var_a, instructions) | self.get_value(var_b, instructions)
        elif 'LSHIFT' in instruction.do:
            split = instruction.do.split('LSHIFT')
            var_a = split[0].strip()
            shift = np.uint16(split[1].strip())
            result = self.get_value(var_a, instructions) << shift
        elif 'RSHIFT' in instruction.do:
            split = instruction.do.split('RSHIFT')
            var_a = split[0].strip()
            shift = np.uint16(split[1].strip())
            result = self.get_value(var_a, instructions) >> shift
        elif 'NOT' in instruction.do:
            split = instruction.do.split('NOT')
            var_a = split[1].strip()
            a = self.get_value(var_a, instructions)
            result = ~a
        else:
            result = self.get_value(instruction.do, instructions)
        
        self.cache[instruction.variable] = result
        return result

def parse(file):
    with open(file, 'r') as f:
        instructions = [Instruction(l.strip()) for l in f]
    return { i.variable: i for i in instructions}

def main():
       
    instructions = parse('input.txt')
    
    machine = Machine()
    a = machine.get_value('a', instructions)
    
    print(f'Pt1: {a}')
    
    new_instructions = instructions.copy()
    new_instructions.pop('b')
    new_instructions['b'] = Instruction(f'{a} -> b')
    
    machine.reset()
    
    a = machine.get_value('a', new_instructions)
    
    print(f'Pt2: {a}')

if __name__ == '__main__':
    main()
