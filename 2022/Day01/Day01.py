from operator import attrgetter

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
    return elves

def get_highest_calorie_count(elves):
    return max(elves, key=attrgetter('total_calories')).total_calories

def main():
    elves = parse('test.txt')
    max_calories = get_highest_calorie_count(elves)
    assert max_calories == 24000

    elves = parse('input.txt')
    max_calories = get_highest_calorie_count(elves)
    
    print(f'Pt1: {max_calories}')

    pass

if __name__ == '__main__':
    main()
