import re

class Stack:
    def __init__(self, nr) -> None:
        self._list = []
        self.nr = nr
    
    def push(self, element):
        self._list.append(element)

    def pop(self):
        return self._list.pop()

    def peek(self):
        return self._list[-1]

    def slice(self, amount):
        s = self._list[-amount:]
        self._list = self._list[:-amount]
        return s

    def drop(self, elements):
        self._list = self._list + elements

class Instruction:
    def __init__(self, from_, to, amount) -> None:
        self.from_ = from_
        self.to = to
        self.amount = amount

def parse(file):
    stack_lines = []
    stacks = []
    instructions = []
    with open(file, 'r') as f:
        for l in f:

            if len(stacks) == 0:
                for match in re.finditer(r'\d+', l):
                    stack = Stack(int(match.group()))
                    for s in reversed(stack_lines):
                        if s[match.start()] != ' ':
                            stack.push(s[match.start()])
                    stacks.append(stack)
                
            if len(stacks) == 0:
                stack_lines.append(l)

            match = re.match(r'^move (\d+) from (\d+) to (\d+)$', l)
            if match:
                instructions.append(Instruction(int(match.group(2)), int(match.group(3)), int(match.group(1))))

    return (stacks, instructions)

def apply_instruction_1(stacks, i):
    source_stack = stacks[i.from_ - 1]
    target_stack = stacks[i.to - 1]
    for _ in range(i.amount):
        target_stack.push(source_stack.pop())

def apply_instruction_2(stacks, i):
    source_stack = stacks[i.from_ - 1]
    target_stack = stacks[i.to - 1]
    s = source_stack.slice(i.amount)
    target_stack.drop(s)

def get_word(stacks):
    return ''.join(map(lambda x: x.peek(), stacks))

def run(file):
    stacks, instructions = parse(file)
    for i in instructions:
        apply_instruction_1(stacks, i)
    word1 = get_word(stacks)
    stacks, instructions = parse(file)
    for i in instructions:
        apply_instruction_2(stacks, i)
    word2 = get_word(stacks)
    return word1, word2

def main():
    result = run('test.txt')
    assert result[0] == 'CMZ'
    assert result[1] == 'MCD'

    result = run('input.txt')
    print(f'Pt1: {result[0]}')
    print(f'Pt2: {result[1]}')

if __name__ == '__main__':
    main()