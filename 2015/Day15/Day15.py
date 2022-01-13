class Ingredient:
    def __init__(self, str: str) -> None:
        import re
        
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

def sum_ingredients_property(amounts, ingredients, property_accessor):
    r = 0
    for i_a in range(len(amounts)):
        r += amounts[i_a] * property_accessor(ingredients[i_a])
    return r

def score(amounts, ingredients):
    capacity = sum_ingredients_property(amounts, ingredients, lambda x: x.capacity)
    durability = sum_ingredients_property(amounts, ingredients, lambda x: x.durability)
    flavor = sum_ingredients_property(amounts, ingredients, lambda x: x.flavor)
    texture = sum_ingredients_property(amounts, ingredients, lambda x: x.texture)
    
    return capacity * durability * flavor * texture

def optimize(ingredients, calories = -1):
    from gekko import GEKKO
    
    m = GEKKO(remote=False)
    x = m.Array(m.Var, len(ingredients), lb=0, ub=100, integer=True)
    
    m.Maximize(score(x, ingredients))
    m.Equation(sum(x) == 100)
    m.Equation(sum_ingredients_property(x, ingredients, lambda x: x.capacity) > 0)
    m.Equation(sum_ingredients_property(x, ingredients, lambda x: x.durability) > 0)
    m.Equation(sum_ingredients_property(x, ingredients, lambda x: x.flavor) > 0)
    m.Equation(sum_ingredients_property(x, ingredients, lambda x: x.texture) > 0)
    if calories > 0:
        m.Equation(sum_ingredients_property(x, ingredients, lambda x: x.calories) == calories)
    m.options.SOLVER = 1
    m.solve(disp=False)
    
    x = [int(i[0]) for i in x]
    
    return score(x, ingredients)

def main():
    ingredients = parse('input.txt')
    
    print(f'Pt1: {optimize(ingredients)}')
    print(f'Pt2: {optimize(ingredients, 500)}')

if __name__ == '__main__':
    main()
