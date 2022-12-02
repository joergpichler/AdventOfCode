

def parse(file) -> list[tuple[str, str]]:
    result = []
    with open(file, 'r') as f:
        for l in f:
            result.append(tuple(l.strip().split(' ')))
    return result

def calc_score(d):
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


def main():
    data = parse('input.txt')
    score = 0
    for d in data:
        score += calc_score(d)
    print(score)

if __name__ == '__main__':
    main()
