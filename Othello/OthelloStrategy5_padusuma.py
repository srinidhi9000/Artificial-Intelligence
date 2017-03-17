import random
import Othello_Core as parent
from Othello_Core import OthelloCore

maxDict = {}
minDict = {}

SQUARE_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]

class OthelloStrategy(OthelloCore):
    
    def __init__(self):
        OthelloCore.__init__(self)
        
    def is_valid(self, move):
        return (move in self.squares())

    def opponent(self, player):
        if player == parent.BLACK:
            return parent.WHITE
        return parent.BLACK

    def find_bracket(self, square, player, board, direction):
        square = square + direction
        if self.is_valid(square):
            if board[square] == player:
                return None

        while self.is_valid(square):
            if board[square] == parent.EMPTY or board[square] == parent.OUTER:
                return None
            if board[square] == player:
                return square
            square = square + direction

    def is_legal(self, move, player, board, directions):
        if not self.is_valid(move):
            return False
        if board[move] != parent.EMPTY:
            return False
        for i in directions:
            if not self.find_bracket(move, player, board, i) == None:
                return True
        return False
        #find bracket up, down, left, and right plus all diagonals
        #if all return none, return false

    def make_move(self, move, player, board):
        board[move] = player
        for i in parent.DIRECTIONS:
            if not self.find_bracket(move, player, board, i) == None:
                self.make_flips(move, player, board, i)
        
            
    def make_flips(self, move, player, board, direction):
        move = move + direction
        while not board[move] == player:
            board[move] = player
            move = move + direction

    def legal_moves(self, player, board):
        moves = []
        for i in self.squares():
            if self.is_legal(i, player, board, parent.DIRECTIONS):
                moves.append(i)
        return moves
    
    def any_legal_move(self, player, board):
        for i in self.squares():
            if self.is_legal(i, player, board, parent.DIRECTIONS):
                return True
        return False

    def next_player(self, board, prev_player):
        if self.any_legal_move(self.opponent(prev_player), board):
            return self.opponent(prev_player)
        if self.any_legal_move(prev_player, board):
            return prev_player
        return None

    def score(self, player, board):
        SCount = 0
        OCount = 0
        for i in board:
            if i == player:
                SCount += 1
            if i == self.opponent(player):
                OCount += 1
        return (SCount - OCount)

    def b_eval(self, board):
        score = 0
        for i in range(len(board)):
            if board[i] == parent.BLACK:
                score = score + SQUARE_WEIGHTS[i]
            if board[i] == parent.WHITE:
                score = score - SQUARE_WEIGHTS[i]
        return score

    def minimax_strategy(self, max_depth):
        def strategy(board, player):
            return self.minimax(board, player, max_depth)
        return strategy

    def minimax(self, board, player, max_d):
        board = self.cop(board)
        if player == parent.BLACK:
            temp = self.max_dfs(board, parent.BLACK, max_d, 0)
            #print(temp[1])
            return temp[1]
        else:
            temp = self.min_dfs(board, parent.WHITE, max_d, 0)
            #print(temp[1])
            return temp[1]
    def max_dfs(self, board, player, max_d, current_d):
        if current_d == max_d:
            if self.score(parent.BLACK, board) > 0:
                return 1, None
            if self.score(parent.BLACK, board) < 0:
                return -1, None
            return 0, None
        v = -100000
        move = -1
        for m in self.legal_moves(player, board):
            cp = self.cop(board)
            cp[m] == player
            if (str(cp), player) in maxDict:
                new_value = maxDict[(str(cp), player)]
            else:
                n = self.next_player(board, player)
                #print(n)
                if n == parent.BLACK:
                    new_value = self.max_dfs(cp, parent.BLACK, max_d, current_d+1)
                elif n == parent.WHITE:
                    new_value = self.min_dfs(cp, parent.WHITE, max_d, current_d+1)
                else:
                    if self.score(parent.BLACK, board) > 0:
                        return 1, None
                    if self.score(parent.BLACK, board) < 0:
                        return -1, None
                    return 0, None
                maxDict[(str(cp), player)] = new_value
            new_value = new_value[0]
            if new_value == 1:
                return 1, m
            if new_value > v:
                v = new_value
                move = m
        return v, move

    def min_dfs(self, board, player, max_d, current_d):
        if current_d == max_d:
            if self.score(parent.BLACK, board) > 0:
                return 1, None
            if self.score(parent.BLACK, board) < 0:
                return -1, None
            return 0, None
        v = 100000
        move = -1
        for m in self.legal_moves(player, board):
            cp = self.cop(board)
            cp[m] == player
            if (str(cp), player) in minDict:
                new_value = minDict[(str(cp), player)]
            else:
                n = self.next_player(board, player)
                #print(n)
                if n == parent.BLACK:
                    new_value = self.max_dfs(cp, parent.BLACK, max_d, current_d+1)
                elif n == parent.WHITE:
                    new_value = self.min_dfs(cp, parent.WHITE, max_d, current_d+1)
                else:
                    if self.score(parent.BLACK, board) > 0:
                        return 1, None
                    if self.score(parent.BLACK, board) < 0:
                        return -1, None
                    return 0, None
                minDict[(str(cp), player)] = new_value
            new_value = new_value[0]
            if new_value == -1:
                return -1, m
            if new_value < v:
                v = new_value
                move = m
        return v, move

    def random(self, board, player):
        temp = self.legal_moves(player, board)
        return random.choice(temp)

#    def best_strategy(self, board, player, best_move, still_running):
#        board = self.cop(s)
#        if player == parent.WHITE:
#            temp = min_dfs()
#            return temp[1]
#        else:
#            temp = max_dfs()
#            return temp[1]

    def cop(self, board):
        N = []
        for i in board:
            N.append(i)
        return N




