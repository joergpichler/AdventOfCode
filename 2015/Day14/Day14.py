import re
from typing import List

class Reindeer:
    def __init__(self, str) -> None:
        split = str.split(' ')
        matches = re.findall(r'\d+', str)
        self.name = split[0]
        self.speed = int(matches[0])
        self.flying_duration = int(matches[1])
        self.resting_duration = int(matches[2])
        
    def __repr__(self) -> str:
        return f'{self.name} {self.speed} km/s for {self.flying_duration}s resting: {self.resting_duration}s'

class ReindeerSimulator:
    def __init__(self, reindeer: Reindeer) -> None:
        self.reindeer = reindeer
        self.flying_timer = self.reindeer.flying_duration
        self.resting_timer = self.reindeer.resting_duration
        self.is_resting = False
        self.distance = 0
        self.ticks = 0
        self.score = 0
        
    def tick(self):
        if not self.is_resting:
            self.flying_timer -= 1
            self.distance += self.reindeer.speed
        else:
            self.resting_timer -= 1
        
        if self.flying_timer == 0:
            self.flying_timer = self.reindeer.flying_duration
            self.is_resting = True
        
        if self.resting_timer == 0:
            self.resting_timer = self.reindeer.resting_duration
            self.is_resting = False
    
    def __repr__(self) -> str:
        return f'{self.reindeer.name} {self.distance}'

def parse(file):
    with open(file, 'r') as f:
        return [Reindeer(l) for l in f]

def race(reindeers: List[Reindeer], ticks):
    reindeer_simulators = [ReindeerSimulator(r) for r in reindeers]
    for _ in range(ticks):
        for s in reindeer_simulators:
            s.tick()
        current_lead_distance = max([s.distance for s in reindeer_simulators])
        for s in [x for x in reindeer_simulators if x.distance == current_lead_distance]:
            s.score += 1
            
    max_dist = reindeer_simulators[0].distance
    for s in reindeer_simulators:
        if s.distance > max_dist:
            max_dist = s.distance
    
    return (max([s.distance for s in reindeer_simulators]), max([s.score for s in reindeer_simulators]))
    
def main():
    reindeers = parse('test.txt')
    results = race(reindeers, 1000)
    assert results[0] == 1120
    assert results[1] == 689
    
    reindeers = parse('input.txt')
    results = race(reindeers, 2503)
    print(f'Pt1: {results[0]}')
    print(f'Pt2: {results[1]}')
    
if __name__ == '__main__':
    main()
