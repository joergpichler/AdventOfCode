class Elf1:

    def __init__(self, number: int) -> None:
        self.number = number
        self.has_presents = True
        
    def __repr__(self) -> str:
        return f'{self.number} {self.has_presents}'


class Elf2:

    def __init__(self, number) -> None:
        self.number = number
        self.next = None
        self.previous = None

    def __repr__(self) -> str:
        return self.number


def main():

    assert play_game_1(5) == 3
    winner = play_game_1(3005290)
    print(f'Winner of part 1 is {winner}')

    assert play_game_2(5) == 2
    winner = play_game_2(3005290)
    print(f'Winner of part 2 is {winner}')


def play_game_1(number_of_elves: int):
    elves = [Elf1(x) for x in range(1, number_of_elves + 1)]
    while(len(elves) > 1):
        for i in range(len(elves)):
            elf = elves[i]
            if not elf.has_presents:
                continue
            next_elf_with_presents = elves[(i + 1) % len(elves)]
            next_elf_with_presents.has_presents = False
        elves = [x for x in elves if x.has_presents]
    return elves[0].number


def play_game_2(number_of_elves: int):
    
    elf = create_elves(number_of_elves)
    target = elf
    for _ in range(int(number_of_elves/2)):
        target = target.next
    
    while elf.next != elf:
        target.previous.next = target.next
        target.next.previous = target.previous
        target = target.next.next if number_of_elves % 2 == 1 else target.next
        number_of_elves -= 1

        elf = elf.next

    return elf.number


def create_elves(number_of_elves: int):
    first_elf = Elf2(1)
    elf = first_elf

    for i in range(2, number_of_elves + 1):
        next_elf = Elf2(i)
        elf.next = next_elf
        next_elf.previous = elf

        elf = next_elf

    first_elf.previous = elf
    elf.next = first_elf

    return first_elf


if __name__ == '__main__':
    main()
