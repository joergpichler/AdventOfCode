from collections import Counter, defaultdict

class Card(object):
    def __init__(self, card) -> None:
        self.card = card

    def __repr__(self) -> str:
        return self.card
    
    @property
    def value(self):
        match self.card:
            case '2':
                return 2
            case '3':
                return 3
            case '4':
                return 4
            case '5':
                return 5
            case '6':
                return 6
            case '7':
                return 7
            case '8':
                return 8
            case '9':
                return 9
            case 'T':
                return 10
            case 'J':
                return 11
            case 'Q':
                return 12
            case 'K':
                return 13
            case 'A':
                return 14
            
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value
    
    def __lt__(self, __value: object) -> bool:
        return self.value < __value.value
    
    def __hash__(self) -> int:
        return hash(self.value)

class Card2(Card):
    def __init__(self, card) -> None:
        super().__init__(card)

    @property
    def value(self):
        if self.card == 'J':
            return 1
        return super().value

class Hand(object):
    def __init__(self, cards, bid) -> None:
        self.cards = cards
        self.bid = bid
        self._type = None

    def _type_from_counter(self, c):
        d = defaultdict(lambda: 0)
        for item in c.items():
            d[item[1]] = d[item[1]] + 1
        if 5 in d:
            return 7
        elif 4 in d:
            return 6
        elif 3 in d:
            if 2 in d:
                return 5
            else:
                return 4
        elif 2 in d:
            if d[2] == 2:
                return 3
            else:
                return 2
        else:
            return 1

    def get_type(self):
        if self._type is not None:
            return self._type
        
        c = Counter(self.cards)
        
        self._type = self._type_from_counter(c)

        return self._type

    def __eq__(self, __value: object) -> bool:
        return self is __value
    
    def __lt__(self, __value: object) -> bool:
        type_self = self.get_type()
        type_other = __value.get_type()
        if type_self != type_other:
            return type_self < type_other
        else:
            for i in range(len(self.cards)):
                my_card = self.cards[i]
                other_card = __value.cards[i]

                if my_card < other_card:
                    return True
                elif my_card > other_card:
                    return False
        
        raise Exception
    
    def __repr__(self) -> str:
        return f'{self.cards} {self.bid}'

class Hand2(Hand):
    def __init__(self, cards, bid) -> None:
        super().__init__(cards, bid)
    
    def get_type(self):
        if self._type is not None:
            return self._type
        
        has_j = any((x.card == 'J' for x in self.cards))

        if not has_j:
            return super().get_type()
        
        count_j = sum(1 for x in self.cards if x.card == 'J')
        c = Counter(filter(lambda x: x.card != 'J' ,self.cards))
        
        highest_key = None
        highest_value = 0

        for key, value in c.items():
            if value > highest_value:
                highest_key = key
                highest_value = value
        c[highest_key] = c[highest_key] + count_j

        self._type = self._type_from_counter(c)

        return self._type

def parse(file, hand_factory, card_factory):

    def to_hand(l):
        split = l.strip().split(' ')
        cards = [card_factory(x) for x in split[0]]
        bid = int(split[1])
        return hand_factory(cards, bid)

    with open(file, 'r') as f:
        return [to_hand(l) for l in f]

def calc_winnings(hands):
    s = sorted(hands)
    result = 0
    for i in range(len(s)):
        result = result + ((i + 1) * s[i].bid)
    return result

def main():
    hands = parse('test.txt', lambda x, y: Hand(x, y), lambda x: Card(x))
    assert calc_winnings(hands) == 6440
    hands = parse('test.txt', lambda x, y: Hand2(x, y), lambda x: Card2(x))
    assert calc_winnings(hands) == 5905
    
    hands = parse('input.txt', lambda x, y: Hand(x, y), lambda x: Card(x))
    print(calc_winnings(hands))
    hands = parse('input.txt', lambda x, y: Hand2(x, y), lambda x: Card2(x))
    print(calc_winnings(hands))

if __name__ == '__main__':
    main()
