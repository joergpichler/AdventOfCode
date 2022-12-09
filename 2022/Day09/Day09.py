import numpy as np

class Instruction:
    def __init__(self, direction, value) -> None:
        self.direction = direction
        self.value = value

def parse(file):
    instructions = []
    with open(file, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            instructions.append(Instruction(l[0], int(l[1])))
    return instructions

def count_tail_positions(instructions):
    head_pos = (0, 0)
    tail_pos = (0, 0)
    tail_pos_set = set()
    tail_pos_set.add(tail_pos)

    def touches(a, b):
        return abs(b[0] - a[0]) <= 1 and abs(b[1] - a[1]) <= 1

    def move_tail():
        nonlocal head_pos, tail_pos, tail_pos_set
        
        if touches(head_pos, tail_pos):
            return

        if head_pos[0] == tail_pos[0] and abs(head_pos[1] - tail_pos[1]) > 1:
            new_tail_pos = (tail_pos[0], tail_pos[1] + np.sign(head_pos[1] - tail_pos[1]))
        elif abs(head_pos[0] - tail_pos[0]) > 1 and head_pos[1] == tail_pos[1]:
            new_tail_pos = (tail_pos[0] + np.sign(head_pos[0] - tail_pos[0]), tail_pos[1])
        # diagonal
        elif (abs(head_pos[0] - tail_pos[0]) == 1 and abs(head_pos[1] - tail_pos[1]) == 2) or \
            (abs(head_pos[0] - tail_pos[0]) == 2 and abs(head_pos[1] - tail_pos[1]) == 1):
            new_tail_pos = (tail_pos[0] + np.sign(head_pos[0] - tail_pos[0]), tail_pos[1] + np.sign(head_pos[1] - tail_pos[1]))
        else:
            raise Exception

        if not touches(head_pos, new_tail_pos):
            raise Exception

        tail_pos = new_tail_pos
        tail_pos_set.add(tail_pos)

    for instruction in instructions:
        if instruction.direction == 'R':
            for _ in range(instruction.value):
                head_pos = (head_pos[0] + 1, head_pos[1])
                move_tail()
        elif instruction.direction == 'L':
            for _ in range(instruction.value):
                head_pos = (head_pos[0] - 1, head_pos[1])
                move_tail()
        elif instruction.direction == 'U':
            for _ in range(instruction.value):
                head_pos = (head_pos[0], head_pos[1] - 1)
                move_tail()
        elif instruction.direction == 'D':
            for _ in range(instruction.value):
                head_pos = (head_pos[0], head_pos[1] + 1)
                move_tail()
        else:
            raise Exception
    
    return len(tail_pos_set)

def main():
    instructions = parse('test.txt')
    assert count_tail_positions(instructions) == 13

    instructions = parse('input.txt')
    print(f'{count_tail_positions(instructions)}')

if __name__ == '__main__':
    main()
