import numpy as np
#instrucciones del othello
class Othello:
    def __init__(self, givenBoard=None):
        self.columns = ['A','B','C','D','E','F','G','H']
        self.set_heuristic = False
        if givenBoard is None:
            self.board = [
                [0,0,0,0,0,0,0,0], \
                [0,0,0,0,0,0,0,0], \
                [0,0,0,0,0,0,0,0], \
                [0,0,0,1,2,0,0,0], \
                [0,0,0,2,1,0,0,0], \
                [0,0,0,0,0,0,0,0], \
                [0,0,0,0,0,0,0,0], \
                [0,0,0,0,0,0,0,0]]
        else:
            self.board = givenBoard
        self.moves = []
        self.last_move = [-1,-1]

    def setHeuristic(self, heuristic):
        self.setHeuristic = True
        self.given_heuristic = heuristic

    def cAvailable(self, y, x, player):
        currBoard = self.board
        if type(x) == int:
            x = x - 1
        else:
            x = int(self.columns[x]) - 1
        y = y - 1
        if x > 7 or y > 7:
            return False

        if self.board[y][x] == 0:
            self.board[y][x] = player
            if (self.checkFlip(x,y)):
                self.moves.append([x,y])
                self.last_move = [x,y]
                return True
            else:
                self.board[y][x] = 0
        # else:
        #     print('Casilla no displonible')
        return False

    def transform(self, number):
        x = number % 8
        y = number / 8
        self.board[y][x] = '1'

    def printBoard(self):
        print('    ', end='')
        for column in self.columns:
            print(column, end='  ')
        print('')
        for idx, x in enumerate(self.board):
            print('{} '.format(idx+1), end=' ')
            print(x)

    def setBoard(self, board):
        self.board = np.array(board).reshape((8, 8)).tolist()

    def reset(self):
        print('new')
        self.board = [
            [0,0,0,0,0,0,0,0], \
            [0,0,0,0,0,0,0,0], \
            [0,0,0,0,0,0,0,0], \
            [0,0,0,1,2,0,0,0], \
            [0,0,0,2,1,0,0,0], \
            [0,0,0,0,0,0,0,0], \
            [0,0,0,0,0,0,0,0], \
            [0,0,0,0,0,0,0,0]]

    def checkFlip(self, x, y):
        player = self.board[y][x]
        if player == 1:
            enemy = 2
        else:
            enemy = 1

        countFails = 0
        for i in range(8):
            if(self.checkDirection(x,y,(i), player, enemy) == False):
                countFails = countFails + 1

        if countFails == 8:
            return False
        return True


    def checkDirection(self, x, y, dir, player, enemy):
        directions = {
            1: [-1,-1] ,
            2: [0,-1 ] ,
            3: [1,-1 ] ,
            4: [-1,0 ] ,
            5: [1,0  ] ,
            6: [-1, 1] ,
            7: [0,1  ] ,
            8: [1, 1 ]
        }
        dir += 1
        vector = directions.get(dir)
        positionToFlip = []
        tmpx = x
        tmpy = y

        while True:
            if dir <= 3:
                if tmpy == 0:
                    positionToFlip = []
                    break
            if dir >= 5:
                if tmpy == 7:
                    positionToFlip = []
                    break
            if dir == 1 or dir == 4 or dir == 6:
                if tmpx == 0:
                    positionToFlip = []
                    break
            if dir == 3 or dir == 5 or dir == 8:
                if tmpx == 7:
                    positionToFlip = []
                    break

            tmpx = tmpx + vector[0]
            tmpy = tmpy + vector[1]

            if self.board[tmpy][tmpx] == enemy:
                positionToFlip.append((tmpx,tmpy))

            elif self.board[tmpy][tmpx] == player:
                self.flip(positionToFlip, player)
                break

            elif self.board[tmpy][tmpx] == 0:
                positionToFlip = []
                break

            else:
                print('[-] Error: null {}'.format(self.board[tmpy][tmpx]))
                break

        if positionToFlip == []:
            return False
        return True

    def flip(self, list_pos, player):
        for x,y in list_pos:
            self.board[y][x] = player
    def Game_Finish(self):
        for x in range(8):
            for y in range(8):
                if self.board[y][x] == 0:
                    return False
        return True

    def Heuristic(self, player, enemy):
        # adds all the players coins
        if self.setHeuristic == True:
            return self.given_heuristic

        positive_points = 0
        negative_points = 0
        for xi in range(8):
            for yi in range(8):
                if self.board[yi][xi] == player:
                    positive_points += 1
                elif self.board[yi][xi] == enemy:
                    negative_points += 1
        result = positive_points - negative_points
        return result
