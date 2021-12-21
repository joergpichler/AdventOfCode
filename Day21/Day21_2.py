from functools import cache

def get_new_pos(pos_p1, pos_p2, next_roll, turn_player):
    pos_p1 = pos_p1 + next_roll if turn_player == 1 else pos_p1
    if pos_p1 > 10:
        pos_p1 -= 10
    pos_p2 = pos_p2 + next_roll if turn_player == 2 else pos_p2
    if pos_p2 > 10:
        pos_p2 -= 10
    return pos_p1, pos_p2

@cache # this is the magic :P
def play_game(game_state):
    pos_p1 = game_state[0]
    pos_p2 = game_state[1]
    score_p1 = game_state[2]
    score_p2 = game_state[3]
    turn_player = game_state[4]
    next_roll = game_state[5]
    roll_no = game_state[6]
    
    if roll_no in [1,2]: # move pawn of active player and start next round
        pos_p1, pos_p2 = get_new_pos(pos_p1, pos_p2, next_roll, turn_player)
        a1, b1 = play_game((pos_p1, pos_p2, score_p1, score_p2, turn_player, 1, roll_no + 1))
        a2, b2 = play_game((pos_p1, pos_p2, score_p1, score_p2, turn_player, 2, roll_no + 1))
        a3, b3 = play_game((pos_p1, pos_p2, score_p1, score_p2, turn_player, 3, roll_no + 1))
        return (a1+a2+a3, b1+b2+b3)
    elif roll_no == 3: # last roll of the round
        pos_p1, pos_p2 = get_new_pos(pos_p1, pos_p2, next_roll, turn_player)
        # add score
        if turn_player == 1:
            score_p1 += pos_p1
            if score_p1 >= 21:
                return (1, 0)
        elif turn_player == 2:
            score_p2 += pos_p2
            if score_p2 >= 21:
                return (0, 1)
        next_player = 2 if turn_player == 1 else 1
        a1, b1 = play_game((pos_p1, pos_p2, score_p1, score_p2, next_player, 1, 1))
        a2, b2 = play_game((pos_p1, pos_p2, score_p1, score_p2, next_player, 2, 1))
        a3, b3 = play_game((pos_p1, pos_p2, score_p1, score_p2, next_player, 3, 1))
        return (a1+a2+a3, b1+b2+b3)
    else:
        raise Exception
    
def main():
    start_p1 = 4
    start_p2 = 8
    start_p1 = 2
    start_p2 = 1
    #0: pos_p1, 1: pos_p2, 2: score_p1, 3: score_p2, 4: turn_player, 5: next_roll 6: roll_no
    a1, b1 = play_game((start_p1, start_p2, 0, 0, 1, 1, 1))
    a2, b2 = play_game((start_p1, start_p2, 0, 0, 1, 2, 1))
    a3, b3 = play_game((start_p1, start_p2, 0, 0, 1, 3, 1))
    
    score1 = a1+a2+a3
    score2 = b1+b2+b3
    
    print(f'{score1 if score1 > score2 else score2}')

if __name__ == '__main__':
    main()
    
