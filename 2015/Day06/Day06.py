import re
from collections import defaultdict

class Instruction:
    def __init__(self, s: str) -> None:
        match = re.match(r'^(.*?)(\d+),(\d+)\sthrough\s(\d+),(\d+)$', s)
        if not match:
            raise Exception
        self.command = match.group(1).strip()
        self.rows = (int(match.group(2)), int(match.group(4)))
        self.columns = (int(match.group(3)), int(match.group(5)))
        
    def __repr__(self) -> str:
        return f'{self.command} rows: {self.rows} columns: {self.columns}'
    
class LightsGrid:
    def __init__(self) -> None:
        self.grid = defaultdict(bool)
        self.brightnessGrid = defaultdict(int)
        
    def run_instruction(self, instruction: Instruction, pt2: bool = False):
        for r in range(instruction.rows[0], instruction.rows[1] + 1):
            for c in range(instruction.columns[0], instruction.columns[1] + 1):
                if instruction.command == 'toggle':
                    self.grid[(r, c)] = not self.grid[(r, c)]
                    self.brightnessGrid[(r, c)] += 2
                elif instruction.command == 'turn on':
                    self.grid[(r, c)] = True
                    self.brightnessGrid[(r, c)] += 1
                elif instruction.command == 'turn off':
                    self.grid[(r, c)] = False
                    if self.brightnessGrid[(r, c)] > 0:
                        self.brightnessGrid[(r, c)] -= 1
                else:
                    raise Exception()
    
    @property
    def count(self):
        count = 0
        for r in range(1000):
            for c in range(1000):
                if self.grid[(r, c)]:
                    count += 1
        return count
    
    @property
    def brightness(self):
        brightness = 0
        for r in range(1000):
            for c in range(1000):
                brightness += self.brightnessGrid[(r, c)]
        return brightness

def parse(file):
    with open(file, 'r') as f:
        return [Instruction(x) for x in f]

def main():
    instructions = parse('input.txt')
    grid = LightsGrid()
    
    for instruction in instructions:
        grid.run_instruction(instruction)
        
    print(f'Pt1: {grid.count}')
    print(f'Pt2: {grid.brightness}')

if __name__ == '__main__':
    main()
