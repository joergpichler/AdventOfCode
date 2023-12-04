import re

class Card:
    def __init__(self, line):
        self._line = line
        split = line.split(':')
        self.number = int(split[0].split(' ')[-1])
        numbers = split[1].split('|')
        winning_numbers = re.findall(r'\d+',  numbers[0])
        self.winning_numbers = list(map(lambda x: int(x), winning_numbers))
        numbers = re.findall(r'\d+', numbers[1])
        self.numbers = list(map(lambda x: int(x), numbers))
        pass

    def pt1(self):
        score = 0
        for number in self.numbers:
            if number in self.winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score = score * 2
        return score
    
    def pt2(self):
        score = 0
        for number in self.numbers:
            if number in self.winning_numbers:
                score = score + 1
        return score

def parse(file):
    cards = []
    with open(file, 'r') as f:
        for l in f:
            cards.append(Card(l.strip()))
    return cards

def pt1(data):
    total = 0
    for card in data:
        total = total + card.pt1()
    return total

def pt2(data):
    cards = { x.number: 1 for x in data }

    for i in range(len(data)):
        card = data[i]
        wins = card.pt2()
        for j in range(card.number + 1, card.number + 1 + wins):
            if j in cards:
                cards[j] = cards[j] + cards[card.number]
        
    return sum(cards.values())

def main():
    data = parse('test.txt')
    assert pt1(data) == 13
    assert pt2(data) == 30

    data = parse('input.txt')
    print(pt1(data))
    print(pt2(data))

if __name__ == '__main__':
    main()
