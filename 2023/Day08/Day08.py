import regex as re
import math

class Node:
    def __init__(self, line) -> None:
        match = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
        self.id = match.groups()[0]
        self.left = match.groups()[1]
        self.right = match.groups()[2]

    def __repr__(self) -> str:
        return f'{self.id} = ({self.left}, {self.right})'

def parse(file):
    with open(file, 'r') as f:
        instructions = f.readline().strip()
        f.readline() # empty line
        line = f.readline()
        nodes = {}
        while line:
            node = Node(line.strip())
            nodes[node.id] = node
            line = f.readline()
    return instructions, nodes

def get_next_node(node, nodes, step):
    if step == 'L':
        next_node = node.left
    elif step == 'R':
        next_node = node.right
    node = nodes[next_node]
    return node

def pt1(instructions, nodes):
    node = nodes['AAA']
    counter = 0
    while node.id != 'ZZZ':
        step = instructions[counter % len(instructions)]
        node = get_next_node(node, nodes, step)
        counter = counter + 1
    return counter

def get_cycle(node, nodes, instructions):
    counter = 0
    while node.id[2] != 'Z':
        step = instructions[counter % len(instructions)]
        node = get_next_node(node, nodes, step)
        counter = counter + 1
    return counter

def pt2(instructions, nodes: dict):
    current_nodes = [x for x in nodes.values() if x.id[2] == 'A']
    for i in range(len(current_nodes)):
         node = current_nodes[i]
         current_nodes[i] = get_cycle(node, nodes, instructions)
    return math.lcm(*current_nodes)
    
def main():
    instructions, nodes = parse('test.txt')
    assert pt1(instructions, nodes) == 2
    instructions, nodes = parse('test2.txt')
    assert pt1(instructions, nodes) == 6
    instructions, nodes = parse('test3.txt')
    assert pt2(instructions, nodes) == 6

    instructions, nodes = parse('input.txt')
    print(pt1(instructions, nodes))
    print(pt2(instructions, nodes))

if __name__ == '__main__':
    main()
