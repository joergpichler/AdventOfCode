import re
import numpy as np

class BingoBoard:
    def __init__(self, board) -> None:
        self.board = np.array(board)
        
    def callNumber(self, number):
        result = np.where(self.board == number)
        coords = list(zip(result[0], result[1]))
        if(len(coords) == 0):
            return
        elif(len(coords) == 1):
            self.board[coords[0][0], coords[0][1]] = -1
        else:
            raise Exception
        
    def wins(self):
        vector = np.full(self.board.shape[0], -1)
        colWin = np.equal(vector, self.board).all(axis=0).any()
        rowWin = np.equal(vector, self.board).all(axis=1).any()
        return colWin or rowWin
    
    def getScore(self):
        score = 0
        for x in np.nditer(self.board):
            if(x != -1):
                score += x
        return score

def getNumbersAndBoards():
    with open('input.txt', 'r') as f:
        numbers = list(map(int, f.readline().split(',')))
        f.readline() #empty line
        
        boards = []
        board = []
        
        for line in f:
            strippedLine = line.strip()
            if(strippedLine == ''):
                boards.append(board)
                board = []
            else:
                board.append(list(map(int, re.split(r"\s+", strippedLine))))
        
        boards.append(board)
        return [numbers, list(map(BingoBoard, boards))]

def main():
    numbers, boards = getNumbersAndBoards()
    
    firstWinner = None
    
    for number in numbers:
        
        for board in boards:
            board.callNumber(number)
            
        winners = list(filter(lambda x: x.wins(), boards))
        
        if(len(winners) > 0):
            if firstWinner is None:
                firstWinner = winners[0]
                print(f'Pt 1: Winner score: {firstWinner.getScore() * number}')
                
        boards = [b for b in boards if b not in winners]
        
        if(len(boards) == 0):
            if(len(winners) > 1):
                raise Exception
            print(f"Pt 2: Last winner score: {winners[0].getScore() * number}")
            break
    
if __name__ == '__main__':
    main()