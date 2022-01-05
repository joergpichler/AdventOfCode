var cache = new Dictionary<string, (long, long)>();

// for some reason it does not work if hash is done via HashCode.Combine()
string Hash(int posP1, int posP2, int scoreP1, int scoreP2, int turnPlayer, int nextRoll, int rollNo) => 
    $"{posP1}_{posP2}_{scoreP1}_{scoreP2}_{turnPlayer}_{nextRoll}_{rollNo}";

(int, int) GetNewPos(int posP1, int posP2, int nextRoll, int turnPlayer)
{
    posP1 = turnPlayer == 1 ? posP1 + nextRoll : posP1;
    posP2 = turnPlayer == 2 ? posP2 + nextRoll : posP2;
    if (posP1 > 10)
        posP1 -= 10;
    if (posP2 > 10)
        posP2 -= 10;
    return (posP1, posP2);
}

(long, long) PlayGame(int posP1, int posP2, int scoreP1, int scoreP2, int turnPlayer, int nextRoll, int rollNo)
{
    var hash = Hash(posP1, posP2, scoreP1, scoreP2, turnPlayer, nextRoll, rollNo);
    if (cache.ContainsKey(hash))
    {
        return cache[hash];
    }

    if (rollNo == 1 || rollNo == 2)
    {
        (posP1, posP2) = GetNewPos(posP1, posP2, nextRoll, turnPlayer);
        (long a1, long b1) = PlayGame(posP1, posP2, scoreP1, scoreP2, turnPlayer, 1, rollNo + 1);
        (long a2, long b2) = PlayGame(posP1, posP2, scoreP1, scoreP2, turnPlayer, 2, rollNo + 1);
        (long a3, long b3) = PlayGame(posP1, posP2, scoreP1, scoreP2, turnPlayer, 3, rollNo + 1);
        var result = (a1 + a2 + a3, b1 + b2 + b3);
        cache[hash] = result;
        return result;
    }
    else if (rollNo == 3)
    {
        (posP1, posP2) = GetNewPos(posP1, posP2, nextRoll, turnPlayer);
        if (turnPlayer == 1)
        {
            scoreP1 += posP1;
            if (scoreP1 >= 21)
            {
                return (1, 0);
            }
        }
        else if (turnPlayer == 2)
        {
            scoreP2 += posP2;
            if (scoreP2 >= 21)
            {
                return (0, 1);
            }
        }
        else
        {
            throw new Exception();
        }

        var nextPlayer = turnPlayer == 1 ? 2 : 1;
        (long a1, long b1) = PlayGame(posP1, posP2, scoreP1, scoreP2, nextPlayer, 1, 1);
        (long a2, long b2) = PlayGame(posP1, posP2, scoreP1, scoreP2, nextPlayer, 2, 1);
        (long a3, long b3) = PlayGame(posP1, posP2, scoreP1, scoreP2, nextPlayer, 3, 1);
        var result = (a1 + a2 + a3, b1 + b2 + b3);
        cache[hash] = result;
        return (a1 + a2 + a3, b1 + b2 + b3);
    }
    else
    {
        throw new Exception();
    }
}

var startP1 = 4;
var startP2 = 8;

(long a1, long b1) = PlayGame(startP1, startP2, 0, 0, 1, 1, 1);
(long a2, long b2) = PlayGame(startP1, startP2, 0, 0, 1, 2, 1);
(long a3, long b3) = PlayGame(startP1, startP2, 0, 0, 1, 3, 1);

var score1 = a1 + a2 + a3;
var score2 = b1 + b2 + b3;

Console.WriteLine($"{Math.Max(score1, score2)}");