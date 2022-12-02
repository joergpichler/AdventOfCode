def parse(file) -> list[tuple[str, str]]:
    result = []
    with open(file, 'r') as f:
        for l in f:
            result.append(tuple(l.strip().split(' ')))
    return result

def calc_score_1(d):
    score = 0
    match d[1]:
        case "X":
            score += 1
        case "Y":
            score += 2
        case "Z":
            score += 3
    if d[0] == 'A':
        if d[1] == 'X':
            score += 3
        elif d[1] == 'Y':
            score += 6
    elif d[0] == 'B':
        if d[1] == 'Y':
            score += 3
        elif d[1] == 'Z':
            score += 6
    elif d[0] == 'C':
        if d[1] == 'X':
            score += 6
        elif d[1] == 'Z':
            score += 3
    return score

def calc_score_2(d):
    score = 0
    decisions = ['A', 'B', 'C']
    decision_scores = {'A':1,'B':2,'C':3}

    if d[1] == 'X': #lose
        my_decision = decisions[decisions.index(d[0]) - 1]
    elif d[1] == 'Y': 
        my_decision = d[0]
        score += 3
    elif d[1] == 'Z':
        my_decision = decisions[(decisions.index(d[0]) + 1) % len(decisions)]
        score += 6

    score += decision_scores[my_decision]
    return score

def calc_scores(data):
    score1 = 0
    score2 = 0
    for d in data:
        score1 += calc_score_1(d)
        score2 += calc_score_2(d)
    return (score1, score2)

def main():
    data = parse('test.txt')
    scores = calc_scores(data)
    assert scores[0] == 15
    assert scores[1] == 12

    data = parse('input.txt')
    scores = calc_scores(data)
    print(f'Pt1: {scores[0]}')
    print(f'Pt2: {scores[1]}')

if __name__ == '__main__':
    main()
