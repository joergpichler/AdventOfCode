import re

class Stack:
    def __init__(self, nr, iterable) -> None:
        self._list = []
        self.nr = nr
        for i in iterable:
            self.push(i)
    
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
    instructions = []
    with open(file, 'r') as f:
        for l in f:
            match = re.match(r'^move (\d+) from (\d+) to (\d+)$', l)
            if match:
                instructions.append(Instruction(int(match.group(2)), int(match.group(3)), int(match.group(1))))
    return instructions

def apply_instruction_2(stacks, i):
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

def get_test_stacks():
    return [Stack(1, ['Z', 'N']),
    Stack(2, ['M', 'C', 'D']),
    Stack(3, ['P'])]

def get_stacks():
    return [Stack(1, ['W', 'D', 'G', 'B', 'H', 'R', 'V']),
    Stack(2, ['J', 'N', 'G', 'C', 'R', 'F']),
    Stack(3, ['L', 'S', 'F', 'H', 'D', 'N', 'J']),
    Stack(4, ['J', 'D', 'S', 'V']),
    Stack(5, ['S', 'H', 'D', 'R', 'Q', 'W', 'N', 'V']),
    Stack(6, ['P', 'G', 'H', 'C', 'M']),
    Stack(7, ['F', 'J', 'B', 'G', 'L', 'Z', 'H', 'C']),
    Stack(8, ['S', 'J', 'R']),
    Stack(9, ['L', 'G', 'S', 'R', 'B', 'N', 'V', 'M'])]

def main():
    test_stacks = get_test_stacks()

    instructions = parse('test.txt')
    for i in instructions:
        apply_instruction_2(test_stacks, i)
    
    word = get_word(test_stacks)
    print(word)

    stacks = get_stacks()

    instructions = parse('input.txt')
    for i in instructions:
        apply_instruction_2(stacks, i)
    
    word = get_word(stacks)
    print(word)

if __name__ == '__main__':
    main()