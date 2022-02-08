from typing import List


class Disc:
    
    def __init__(self, text) -> None:
        import re
        match = re.match(r'^Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).$', text)
        if match is None:
            raise ValueError(f'{text} could not be parsed')
        self.number = int(match.group(1))
        self.total_positions = int(match.group(2))
        self.initial_position = int(match.group(3))
        self.current_position = self.initial_position
        
        
    def tick(self, ticks = 1):
        self.current_position = (self.current_position + ticks) % self.total_positions
        
        
    def reset(self):
        self.current_position = self.initial_position


def tick_discs(discs: List[Disc], ticks = 1):
    for disc in discs:
        disc.tick(ticks)
        
        
def reset_discs(discs: List[Disc]):
    for disc in discs:
        disc.reset()


def simulate(discs: List[Disc]):
    time = 0
    solution = -1
    
    while True: # outer loop for button press
        
        # spin discs to initial position
        tick_discs(discs, time)
            
        # 1 tick elapses when the button is pressed
        tick_discs(discs)
        
        for disc in discs:
            if disc.current_position != 0:
                solution = -1
                break
            else:
                tick_discs(discs)
                solution = time
                    
        if solution != -1:
            break
        
        reset_discs(discs)
        
        time += 1
        
    return solution


def parse(file):
    with open(file, 'r') as f:
        return [Disc(l.strip()) for l in f]


def main():
    discs = parse('test.txt')
    assert simulate(discs) == 5
    
    discs = parse('input.txt')
    pt1 = simulate(discs)
    print(f'Pt1: {pt1}')
    
    reset_discs(discs)
    
    discs.append(Disc("Disc #7 has 11 positions; at time=0, it is at position 0."))
    pt2 = simulate(discs)
    print(f'Pt2: {pt2}')


if __name__ == '__main__':
    main()
