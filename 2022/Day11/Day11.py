import re


class Monkey:


    def __init__(self, lines) -> None:
        self._parse(lines)
        self.items_inspected = 0


    def _parse(self, lines):
        self.number = int(re.search(r'\d+', lines[0]).group(0))
        self.items = [int(x) for x in re.findall(r'\d+', lines[1])]
        self.func = eval(compile(f'lambda old: {lines[2].split("=")[1].strip()}', 'generated.py', 'eval'))
        self.div_test = int(re.search(r'divisible by (\d+)', lines[3]).group(1))
        self.true_case = int(re.search(r'If true: throw to monkey (\d+)', lines[4]).group(1))
        self.false_case = int(re.search(r'If false: throw to monkey (\d+)', lines[5]).group(1))


    def __repr__(self) -> str:
        return f'Monkey {self.number}: {" ".join((str(i) for i in self.items))}'


def parse(file):
    monkeys = []
    with open(file, 'r') as f:
        l = f.readline()
        while(l):
            l = l.strip()
            if l.startswith("Monkey"):
                lines = [l]
                for _ in range(5):
                    lines.append(f.readline().strip())
                monkeys.append(Monkey(lines))
            l = f.readline()

    return { m.number: m for m in monkeys }


def play(monkeys, rounds, supermodulo = 0):
    for _ in range(rounds):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            while(len(monkey.items) > 0):
                monkey.items_inspected += 1
                item = monkey.items.pop(0)
                item = monkey.func(item)
                if supermodulo == 0:
                    item = item // 3
                else:
                    item = item % supermodulo
                if item % monkey.div_test == 0:
                    target_monkey = monkeys[monkey.true_case]
                else:
                    target_monkey = monkeys[monkey.false_case]
                target_monkey.items.append(item)
    l = list(sorted((m.items_inspected for m in monkeys.values()), reverse=True))
    return l[0] * l[1]


def get_supermodulo(monkeys):
    supermodulo = 1
    for m in monkeys.values():
        supermodulo *= m.div_test
    return supermodulo


def main():
    monkeys = parse('test.txt')
    assert play(monkeys, 20) == 10605
    monkeys = parse('test.txt')
    assert play(monkeys, 10000, get_supermodulo(monkeys)) == 2713310158

    monkeys = parse('input.txt')
    print(f'{play(monkeys, 20)}')
    monkeys = parse('input.txt')
    print(f'{play(monkeys, 10000, get_supermodulo(monkeys))}')


if __name__ == '__main__':
    main()
