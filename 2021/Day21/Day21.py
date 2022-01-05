class Player:
    def __init__(self, starting_poosition) -> None:
        self.position = starting_poosition
        self.score = 0
        pass
    
class DeterministicDie:
    def __init__(self) -> None:
        self.times_rolled = 0
    
    def roll(self):
        self.times_rolled += 1
        result = self.times_rolled
        while result > 100:
            result -= 100
        return result
    
class Game:
    def __init__(self, player1, player2, die) -> None:
        self.player1 = player1
        self.player2 = player2
        self.die = die
        self.players_turn = 1
        
    def play(self):
        player = self.player1 if self.players_turn == 1 else self.player2
        
        sum = 0
        for _ in range(3):
            sum += self.die.roll()
        player.position += sum
        while player.position > 10:
            player.position -= 10
        player.score += player.position
        
        self.players_turn = 1 if self.players_turn == 2 else 2

def main():
    player1 = Player(2)
    player2 = Player(1)
    die = DeterministicDie()
    game = Game(player1, player2, die)
    while player1.score < 1000 and player2.score < 1000:
        game.play()
    losing_player = player1 if player1.score < player2.score else player2
    
    print(f'Pt1: {losing_player.score * die.times_rolled}')

if __name__ == '__main__':
    main()
