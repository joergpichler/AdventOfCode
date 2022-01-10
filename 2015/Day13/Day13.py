import re
from typing import List
from collections import defaultdict
import numpy as np

class SeatingRule:
    def __init__(self, str: str) -> None:
        split = str.split(' ')
        self.person = split[0]
        self.neighbor = split[-1].strip('.')
        self.what = "gain" if "gain" in str else "lose"
        self.amount = int(re.findall(r"\d+", str)[0])
        
    def __repr__(self) -> str:
        return f'{self.person} {self.what} {self.amount} {self.neighbor}'

class SeatingRules:
    def __init__(self, seating_rules: List[SeatingRule]) -> None:
        self.seating_rules = defaultdict(list)
        for seating_rule in seating_rules:
            self.seating_rules[seating_rule.person].append(seating_rule)
            
    @property
    def person_names(self):
        return self.seating_rules.keys()
    
    def get_happiness(self, person, neighbor):
        rules = self.seating_rules[person]
        if len(rules) == 0:
            return 0
        for r in rules:
            if r.neighbor == neighbor:
                return r.amount if r.what == "gain" else -r.amount
        return 0

class Person:
    def __init__(self, name) -> None:
        self.name = name
        self.happiness = 0

def parse(file):
    with open(file, 'r') as f:
        return SeatingRules([SeatingRule(l.strip()) for l in f])

def seat(person, person_names, already_seated: List[str], permutations: List):
    already_seated.append(person)
    if len(already_seated) == len(person_names):
        permutations.append(already_seated)
        return
    
    for p in person_names:
        if not p in already_seated:
            seat(p, person_names, already_seated.copy(), permutations)
            
def calc_happiness(seat_order, seating_rules: SeatingRules):
    persons = [Person(s) for s in seat_order]
    
    for i in range(len(persons)):
        next = i + 1
        if i == len(persons) - 1:
            next = 0
        
        persons[i].happiness += seating_rules.get_happiness(seat_order[i], seat_order[next])
        persons[i].happiness += seating_rules.get_happiness(seat_order[i], seat_order[i-1])
    
    return sum([p.happiness for p in persons])

def seat_persons(person_names, seating_rules):
    result = None
    for p in person_names:        
        permutations = []
        seat(p, person_names, [], permutations)
        happiness = [calc_happiness(p, seating_rules) for p in permutations]
        idx_max = np.argmax(happiness)
        if result is None:
            result = (happiness[idx_max], permutations[idx_max])
        elif result[0] < happiness[idx_max]:
            result = (happiness[idx_max], permutations[idx_max])
        pass
    return result[0]

def main():
    seating_rules = parse('test.txt')
    
    assert calc_happiness(['Carol', 'Bob', 'Alice', 'David'], seating_rules) == 330
    
    seating_rules = parse('input.txt')
    
    print(f'Pt1: {seat_persons(seating_rules.person_names, seating_rules)}')
    
    including_myself = list(seating_rules.person_names)
    including_myself.append('myself')
    
    print(f'Pt2: {seat_persons(including_myself, seating_rules)}')

if __name__ == '__main__':
    main()
