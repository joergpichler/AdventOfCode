from operator import attrgetter
from typing import Tuple

class Elf:
    def __init__(self) -> None:
        self._calories = []

    def add_calories(self, calories: int) -> None:
        self._calories.append(calories)

    @property
    def total_calories(self) -> int:
        return sum(self._calories)

def parse(file):
    elves = []
    with open(file, 'r') as f:
        elf = Elf()
        for line in (l.strip() for l in f):
            if line == '':
                elves.append(elf)
                elf = Elf()
            else:
                elf.add_calories(int(line))
        elves.append(elf)
    return elves

def calculate(elves: list[Elf]) -> Tuple[int, int]:
    getter = attrgetter('total_calories')
    sorted_list = sorted(elves, key=getter, reverse=True)
    return (sorted_list[0].total_calories, sum(map(getter, sorted_list[:3])))

def main():
    elves = parse('test.txt')
    result = calculate(elves)
    assert result[0] == 24000
    assert result[1] == 45000

    elves = parse('input.txt')
    result = calculate(elves)
    
    print(f'Pt1: {result[0]}')
    print(f'Pt2: {result[1]}')

if __name__ == '__main__':
    main()
