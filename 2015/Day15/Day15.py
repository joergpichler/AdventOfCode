import re
from pulp import *

class Ingredient:
    def __init__(self, str: str) -> None:
        self.name = str.split(' ')[0][:-1]
        m = re.findall(r'-?\d+', str)
        self.capacity = int(m[0])
        self.durability = int(m[1])
        self.flavor = int(m[2])
        self.texture = int(m[3])
        self.calories = int(m[4])
    
    def __repr__(self) -> str:
        return f'{self.name}'

def parse(file):
    with open(file, 'r') as f:
        return [Ingredient(l) for l in f]

def main():
    ingredients = parse('test.txt')
    
    prob = LpProblem("Cookie Problem", LpMaximize)
    
    items = [i.name for i in ingredients]
    capacities = dict(zip(items, [i.capacity for i in ingredients]))
    durabilities = dict(zip(items, [i.durability for i in ingredients]))
    flavors = dict(zip(items, [i.flavor for i in ingredients]))
    textures = dict(zip(items, [i.texture for i in ingredients]))
    
    vars = LpVariable.dicts("Ingredients", items, 1, cat='Integer')
    
    prob += sum([vars[i] * capacities[i] for i in items]) * sum([vars[i] * durabilities[i] for i in items]) + sum([vars[i] * flavors[i] for i in items]) + sum([vars[i] * textures[i] for i in items])
    
    prob += lpSum([vars[i] for i in items]) == 100, "total"
    prob += lpSum([capacities[i] * vars[i] for i in items]) >= 1, "capacities"
    prob += lpSum([durabilities[i] * vars[i] for i in items]) >= 1, "durabilities"
    prob += lpSum([flavors[i] * vars[i] for i in items]) >= 1, "flavors"
    prob += lpSum([textures[i] * vars[i] for i in items]) >= 1, "textures"
    
    prob.solve()
    
    print(f'{LpStatus[prob.status]}')
    for v in prob.variables():
        print(v.name, ' = ', v.varValue)
    
    pass

if __name__ == '__main__':
    main()
