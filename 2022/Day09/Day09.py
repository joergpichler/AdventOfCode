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

def count_tail_positions(instructions, tail_len = 1):
    head_pos = (0, 0)
    tail = [(0, 0)] * tail_len
    tail_pos_set = set()
    tail_pos_set.add(tail[-1])

    def touches(a, b):
        return abs(b[0] - a[0]) <= 1 and abs(b[1] - a[1]) <= 1

    def move_tail(pos, tail_idx):
        nonlocal tail, tail_pos_set
        
        if tail_idx >= len(tail):
            return

        tail_pos = tail[tail_idx]

        if touches(pos, tail_pos):
            return

        if pos[0] == tail_pos[0] and abs(pos[1] - tail_pos[1]) > 1:
            new_tail_pos = (tail_pos[0], tail_pos[1] + np.sign(pos[1] - tail_pos[1]))
        elif abs(pos[0] - tail_pos[0]) > 1 and pos[1] == tail_pos[1]:
            new_tail_pos = (tail_pos[0] + np.sign(pos[0] - tail_pos[0]), tail_pos[1])
        # diagonal
        elif (abs(pos[0] - tail_pos[0]) == 1 and abs(pos[1] - tail_pos[1]) == 2) or \
            (abs(pos[0] - tail_pos[0]) == 2 and abs(pos[1] - tail_pos[1]) == 1) or \
            (abs(pos[0] - tail_pos[0]) == 2 and abs(pos[1] - tail_pos[1]) == 2):
            new_tail_pos = (tail_pos[0] + np.sign(pos[0] - tail_pos[0]), tail_pos[1] + np.sign(pos[1] - tail_pos[1]))
        else:
            raise Exception

        if not touches(pos, new_tail_pos):
            raise Exception

        tail[tail_idx] = new_tail_pos

        if tail_idx == len(tail) - 1:
            tail_pos_set.add(new_tail_pos)

        move_tail(new_tail_pos, tail_idx + 1)

    for instruction in instructions:
        if instruction.direction == 'R':
            for _ in range(instruction.value):
                head_pos = (head_pos[0] + 1, head_pos[1])
                move_tail(head_pos, 0)
        elif instruction.direction == 'L':
            for _ in range(instruction.value):
                head_pos = (head_pos[0] - 1, head_pos[1])
                move_tail(head_pos, 0)
        elif instruction.direction == 'U':
            for _ in range(instruction.value):
                head_pos = (head_pos[0], head_pos[1] - 1)
                move_tail(head_pos, 0)
        elif instruction.direction == 'D':
            for _ in range(instruction.value):
                head_pos = (head_pos[0], head_pos[1] + 1)
                move_tail(head_pos, 0)
        else:
            raise Exception
    
    return len(tail_pos_set)

def main():
    instructions = parse('test.txt')
    assert count_tail_positions(instructions) == 13
    assert count_tail_positions(instructions, 9) == 1

    instructions = parse('test2.txt')
    assert count_tail_positions(instructions, 9) == 36

    instructions = parse('input.txt')
    print(f'{count_tail_positions(instructions)}')
    print(f'{count_tail_positions(instructions, 9)}')

if __name__ == '__main__':
    main()
