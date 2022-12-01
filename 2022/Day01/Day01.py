from operator import attrgetter

class Elf:
    def __init__(self) -> None:
        self._calories = []

    def add_calories(self, calories: int) -> None:
        self._calories.append(calories)

    @property
    def total_calories(self) -> int:
        return sum(self._calories)

    def __repr__(self) -> str:
        return str(self.total_calories)

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

def get_highest_calorie_count(elves):
    return max(elves, key=attrgetter('total_calories')).total_calories

def get_top3_calorie_count(elves):
    sorted_list = sorted(elves, key=attrgetter('total_calories'), reverse=True)
    return sorted_list[0].total_calories + sorted_list[1].total_calories + sorted_list[2].total_calories

def main():
    elves = parse('test.txt')
    assert get_highest_calorie_count(elves) == 24000
    assert get_top3_calorie_count(elves) == 45000

    elves = parse('input.txt')
    max_calories = get_highest_calorie_count(elves)
    top3_calories = get_top3_calorie_count(elves)
    
    print(f'Pt1: {max_calories}')
    print(f'Pt2: {top3_calories}')

    pass

if __name__ == '__main__':
    main()
