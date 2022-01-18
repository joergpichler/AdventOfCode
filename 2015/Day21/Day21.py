from typing import List
from itertools import permutations

class Weapon:
    def __init__(self, name: str, cost: int, damage: int) -> None:
        self.name = name
        self.cost = cost
        self.damage = damage
        
    def __repr__(self) -> str:
        return f'{self.name}: {self.cost}$ {self.damage} DMG'

class Armor:
    def __init__(self, name: str, cost: int, armor: int) -> None:
        self.name = name
        self.cost = cost
        self.armor = armor
        
    def __repr__(self) -> str:
        return f'{self.name}: {self.cost}$ {self.armor} ARM'
    
class Ring:
    def __init__(self, name: str, cost: int, damage: int, armor: int) -> None:
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor
        
    def __repr__(self) -> str:
        return f'{self.name}: {self.cost}$ {self.damage} DMG {self.armor} ARM'

class Character:
    def __init__(self, weapon: Weapon, armor: Armor, rings: List[Ring]) -> None:
        self.hit_points = 100
        self.weapon = weapon
        self.armor_eq = armor
        self.rings = rings
        
        self.damage = weapon.damage + (0 if rings[0] is None else rings[0].damage) + (0 if rings[1] is None else rings[1].damage)
        self.armor = (0 if armor is None else armor.armor) + (0 if rings[0] is None else rings[0].armor) + (0 if rings[1] is None else rings[1].armor)
        
    def __repr__(self) -> str:
        return f'{self.hit_points} HP {self.weapon} {self.armor_eq} {self.rings}'
    
class Boss:
    def __init__(self, hit_points: int, damage: int, armor: int) -> None:
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor
        pass
    
    def __repr__(self) -> str:
        return f'{self.hit_points} HP {self.damage} DMG {self.armor} ARM'

def parse(file: str):
    weapons = []
    armors = []
    rings = []
    parsing_type = ''
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            if "Weapons" in line:
                parsing_type = 'weapons'
            elif "Rings" in line:
                parsing_type = 'rings'
            elif "Armor" in line:
                parsing_type = 'armor'
            elif len(line) > 0:
                split = [s for s in line.split(' ') if s]
                if parsing_type == 'weapons':
                    weapons.append(Weapon(split[0], int(split[1]), int(split[2])))
                elif parsing_type == 'armor':
                    armors.append(Armor(split[0], int(split[1]), int(split[3])))
                    pass
                elif parsing_type == 'rings':
                    rings.append(Ring(split[0] + ' ' + split[1], int(split[2]), int(split[3]), int(split[4])))
                    pass
            
            line = f.readline()
    return weapons, armors, rings

def fight(character: Character, boss: Boss):
    character_hp = character.hit_points
    boss_hp = boss.hit_points
    
    for i in range(min([character.hit_points, boss.hit_points])):
        character_dmg = max([1, character.damage - boss.armor])
        boss_hp -= character_dmg
        
        if boss_hp <= 0:
            #print(f'Character wins in round {i} with {character_hp} HP left')
            return character
        
        boss_dmg = max([1, boss.damage - character.armor])
        character_hp -= boss_dmg
        
        if character_hp <= 0:
            #print(f'Boss wins in round {i} with {boss_hp} HP left')
            return boss
        
    raise Exception()

def create_character(weapons: List[Weapon], armors: List[Armor], rings: List[Ring]):
    for weapon in weapons:
        for idx_armor in range(-1,len(armors)):
            armor = None if idx_armor == -1 else armors[idx_armor]
            yield Character(weapon, armor, [None, None])
            for perm in permutations([None] + list(range(len(rings))), 2):
                ring1 = None if perm[0] is None else rings[perm[0]]
                ring2 = None if perm[1] is None else rings[perm[1]]
                yield Character(weapon, armor, [ring1, ring2])

def get_equipment_cost(character: Character):
    cost = character.weapon.cost
    if character.armor_eq is not None:
        cost += character.armor_eq.cost
    for ring in character.rings:
        if ring is not None:
            cost += ring.cost
    return cost

def main():
    weapons, armor, rings = parse('shop.txt')
    
    boss = Boss(109, 8, 2)
    
    min_cost = 1000
    max_cost = 0
    
    for character in create_character(weapons, armor, rings):
        winner = fight(character, boss)
        if winner == character:
            min_cost = min(min_cost, get_equipment_cost(character))
        elif winner == boss:
            max_cost = max(max_cost, get_equipment_cost(character))
    
    print(f'Pt1: {min_cost}')
    print(f'Pt2: {max_cost}')

if __name__ == '__main__':
    main()