from collections import deque
import re

import numpy as np


class Screen:
    def __init__(self, rows, columns) -> None:
        self.pixels = np.full((rows, columns), False, bool)


    def _turn_on(self, width, height):
        for col in range(width):
            for row in range(height):
                self.pixels[(row, col)] = True


    def _rotate_row(self, row_idx, amount):
        row = deque(self.pixels[row_idx,:])
        row.rotate(amount)
        self.pixels[row_idx,:] = row


    def _rotate_column(self, col_idx, amount):
        col = deque(self.pixels[:,col_idx])
        col.rotate(amount)
        self.pixels[:,col_idx] = col


    def _run_instruction(self, instruction):
        if "rect" in instruction:
            split = instruction.split(' ')[1].split('x')
            width = int(split[0])
            height = int(split[1])
            self._turn_on(width, height)
        elif "row" in instruction:
            match = re.search(r"y=(\d+) by (\d+)", instruction)
            row = int(match.group(1))
            amount = int(match.group(2))
            self._rotate_row(row, amount)
        elif "column" in instruction:
            match = re.search(r"x=(\d+) by (\d+)", instruction)
            column = int(match.group(1))
            amount = int(match.group(2))
            self._rotate_column(column, amount)


    def run_instructions(self, instructions):
        for instruction in instructions:
            self._run_instruction(instruction)


    def get_active_pixels(self):
        return self.pixels.sum()


    def print(self, char='\u2588'):
        for row in range(self.pixels.shape[0]):
            row_str =''
            for col in range(self.pixels.shape[1]):
                row_str += char if self.pixels[(row,col)] else ' '
            print(row_str)


def parse(file):
    with open(file, 'r') as f:
        return [l.strip() for l in f]


def main():
    instructions = parse('test.txt')
    screen = Screen(3, 7)
    screen.run_instructions(instructions)
    assert screen.get_active_pixels() == 6
    
    instructions = parse('input.txt')
    screen = Screen(6, 50)
    screen.run_instructions(instructions)
    print(f'Pt1: {screen.get_active_pixels()}')
    screen.print()


if __name__ == '__main__':
    main()