from collections import namedtuple
from dataclasses import dataclass

@dataclass
class Coords1:
    forward: int
    depth: int

@dataclass
class Coords2:
    forward: int
    depth: int
    aim: int

Command = namedtuple('Command', 'action value')

def parseLine(line):
    split = line.split()
    return Command(split[0], int(split[1]))

def applyCommand(command: Command, coords1: Coords1):
    if(command.action == 'forward'):
        coords1.forward += command.value
    elif(command.action == 'down'):
        coords1.depth += command.value
    elif(command.action == 'up'):
        coords1.depth -= command.value
        
def applyCommand2(command: Command, coords2: Coords2):
    if(command.action == 'forward'):
        coords2.forward += command.value
        coords2.depth += coords2.aim * command.value
    elif(command.action == 'down'):
        coords2.aim += command.value
    elif(command.action == 'up'):
        coords2.aim -= command.value
    
testFile = open('input.txt', 'r')
commands = list(map(parseLine, testFile.readlines())) # map strings to int

coords1 = Coords1(0, 0)

for command in commands:
    applyCommand(command, coords1)

print(f"Horizontal Pos {coords1.forward} Depth {coords1.depth} Result {coords1.forward * coords1.depth}")

coords2 = Coords2(0, 0, 0)

for command in commands:
    applyCommand2(command, coords2)
    
print(f"Horizontal Pos {coords2.forward} Depth {coords2.depth} Result {coords2.forward * coords2.depth}")