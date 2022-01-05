from collections import defaultdict

def parse(file):
    with open(file, 'r') as f:
        return f.readline()

def visitHouses(instructions: str, noOfSantas: int = 1):
    houses = defaultdict(int)
    locations = []
    
    for _ in range(noOfSantas):
        locations.append((0, 0))
        
    for location in locations:
        houses[location] += 1
        
    for i in range(len(instructions)):
        c = instructions[i]
        
        location = locations[i % noOfSantas]
        
        if c == '<':
            location = (location[0] - 1, location[1])
        elif c == '^':
            location = (location[0], location[1] - 1)
            pass
        elif c == '>':
            location = (location[0] + 1, location[1])
            pass
        elif c == 'v':
            location = (location[0], location[1] + 1)
            pass
        else:
            raise Exception()
        
        locations[i % noOfSantas] = location
        houses[location] += 1
        
    return houses

def main():
    assert len(visitHouses('>')) == 2
    assert len(visitHouses('^>v<')) == 4
    assert len(visitHouses('^v^v^v^v^v')) == 2
    
    instructions = parse('input.txt')
    
    print(f'Pt1: {len(visitHouses(instructions))}')
    
    assert len(visitHouses('^v', 2)) == 3
    assert len(visitHouses('^>v<', 2)) == 3
    assert len(visitHouses('^v^v^v^v^v', 2)) == 11
    
    print(f'Pt2: {len(visitHouses(instructions, 2))}')
    
if __name__ == '__main__':
    main()
