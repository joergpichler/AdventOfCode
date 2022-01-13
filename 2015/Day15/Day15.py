import re
from typing import Callable, List

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

def calc_optimum_1(ingredients: List[Ingredient], amounts: List[int], optimum: List):
    capacity = 0
    durability = 0
    flavor = 0
    texture = 0
    
    for i_a in range(len(amounts)):
        capacity += amounts[i_a] * ingredients[i_a].capacity
        durability += amounts[i_a] * ingredients[i_a].durability
        flavor += amounts[i_a] * ingredients[i_a].flavor
        texture += amounts[i_a] * ingredients[i_a].texture
        
    if capacity > 0 and durability > 0 and flavor > 0 and texture > 0:
        score = capacity * durability * flavor * texture
        if score > optimum[0]:
            optimum[0] = score
            optimum[1] = amounts.copy()
            
def calc_optimum_2(ingredients: List[Ingredient], amounts: List[int], optimum: List):
    capacity = 0
    durability = 0
    flavor = 0
    texture = 0
    calories = 0
    
    for i_a in range(len(amounts)):
        capacity += amounts[i_a] * ingredients[i_a].capacity
        durability += amounts[i_a] * ingredients[i_a].durability
        flavor += amounts[i_a] * ingredients[i_a].flavor
        texture += amounts[i_a] * ingredients[i_a].texture
        calories += amounts[i_a] * ingredients[i_a].calories
        
    if calories == 500 and capacity > 0 and durability > 0 and flavor > 0 and texture > 0:
        score = capacity * durability * flavor * texture
        if score > optimum[0]:
            optimum[0] = score
            optimum[1] = amounts.copy()

def add_ingredient(ingredients: List[Ingredient], ingredient_index, amounts: List[int], optimum: List, total_ingredients: int, fun: Callable):
    for i in range(101):
        amounts[ingredient_index] = i
        
        if sum(amounts) == total_ingredients and ingredient_index == len(ingredients) - 1:
            fun(ingredients, amounts, optimum) 
        elif sum(amounts) > total_ingredients:
            pass
        elif ingredient_index < len(ingredients) - 1:
            add_ingredient(ingredients, ingredient_index + 1, amounts, optimum, total_ingredients, fun)
            
    amounts[ingredient_index] = 0
            

def calc_optimum(ingredients: List[Ingredient], fun):
    amounts = [0] * len(ingredients)
    optimum = [0] * 2
    add_ingredient(ingredients, 0, amounts, optimum, 100, fun)
    return optimum

def main():
    ingredients = parse('input.txt')
    
    optimum = calc_optimum(ingredients, calc_optimum_1)
    print(f'Pt1: {optimum[0]} ({optimum[1]})')
    
    optimum = calc_optimum(ingredients, calc_optimum_2)
    print(f'Pt2: {optimum[0]} ({optimum[1]})')

    pass

if __name__ == '__main__':
    main()
