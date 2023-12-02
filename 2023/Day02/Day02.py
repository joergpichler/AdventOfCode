import numpy as np

class Game:
    def __init__(self, str) -> None:
        self.__parse(str)
        
    def __parse(self, line: str):
        split = line.split(':')
        self.id = int(split[0].split(' ')[1])
        sets = split[1].split(';')
        self.sets = []
        for set in sets:
            self.sets.append([x.strip() for x in set.split(',')])
        pass

def parse(file):
    with open(file, 'r') as f:
        return [Game(l.strip()) for l in f]

def play_game_1(games, dict):
    total = 0
    for game in games:
        game_possible = True
        for set in game.sets:
            for draw in set:
                split = draw.split(' ')
                num = int(split[0])
                color = split[1]
                if(dict[color] < num):
                    game_possible = False
                    break
            if not game_possible:
                break
        if game_possible:
            total = total + game.id
    return total

def play_game_2(games):
    total = 0
    for game in games:
        dict = { 'red': 0, 'green': 0, 'blue': 0 }
        for set in game.sets:
            for draw in set:
                split = draw.split(' ')
                num = int(split[0])
                color = split[1]
                dict[color] = max(dict[color], num)
        total = total + np.prod(list(dict.values()))
    return total

def main():
    games = parse('test.txt')
    assert play_game_1(games, {'red': 12, 'green': 13, 'blue': 14}) == 8
    assert play_game_2(games) == 2286
    games = parse('input.txt')
    print(play_game_1(games, {'red': 12, 'green': 13, 'blue': 14}))
    print(play_game_2(games))

if __name__ == '__main__':
    main()
