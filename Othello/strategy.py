# SRINIDHI KRISHNAN #

import Othello_Core as core
import random
import os, signal
import time
from multiprocessing import Process, Value
time_limit = 5
d = {}
nodes = 0

import pickle

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

MAX = BLACK
MIN = WHITE

class Strategy(core.OthelloCore):
    def squares(self):
        """List all the valid squares on the board."""
        return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

    def is_valid(self, move):
        """Is move a square on the board?"""
        if(move > 10 and move < 89 and move%10 > 0 and move%10 < 9):
            return True
        return False

    def opponent(self, player):
        """Get player's opponent piece."""
        if(player == BLACK):
            return WHITE
        else:
            return BLACK

    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        Returns the index of the bracketing square if found
        """
        pos = square + direction
        if board[pos] == player:
            return None
        while board[pos] == self.opponent(player):
            pos += direction
        if(board[pos] == EMPTY or board[pos] == OUTER):
            return None
        else:
            return pos

    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        #hasbracket = lambda direction: self.find_bracket(move, player, board, direction)
        #return board[move] == EMPTY and any(map(hasbracket, DIRECTIONS))
        if(board[move] == EMPTY):
            for d in DIRECTIONS:
                if(self.find_bracket(move, player, board, d) is not None):
                    return True
        return False

    ### Making moves
    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    def make_move(self, move, player, board):
        """Update the board to reflect the move by the specified player."""
        l = board
        l[move] = player
        for d in DIRECTIONS:
            self.make_flips(move, player, l, d)
        return l

    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        br = self.find_bracket(move, player, board, direction)
        if(br == None):
            return
        curr = direction + move
        while curr != br:
            board[curr] = player
            curr += direction

    def count(self, board):
        b = 0
        w = 0
        for e in board:
            if e == '@':
                b +=1
            elif e =='o':
                w+=1
        return (b,w)

    def legal_moves(self, player, board):
        """Get a list of all legal moves for player, as a list of integers"""
        #return [sq for sq in self.squares() if self.is_legal(sq, player, board)]
        l = []
        for s in self.squares():
            if(self.is_legal(s, player, board)):
                l.append(s)
        random.shuffle(l)
        return l

    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
        l = self.legal_moves(player, board)
        if(len(l) > 0):
            return True
        return False

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        opp = self.opponent(prev_player)
        if(not self.any_legal_move(opp, board)):
            if(not self.any_legal_move(prev_player, board)):
                return None
            else:
                return prev_player
        else:
            return opp

    def score(self, player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        p = 0
        o = 0
        opp = self.opponent(player)
        for s in board:
            if(s == player):
                p+=1
            if(s == opp):
                o+=1
        return p-o

    def random_strategy(self):
        def strategy(board, player):
            l = self.legal_moves(player, board)
            return random.choice(l)
        return strategy

    def human_strategy(self):
        def strategy(board, player):
            move = int(input("Move (11-88): "))
            while move not in self.legal_moves(player, board):
                move = int(input("Move (11-88): "))
            return move
        return strategy


    def eval(self, board):
        SQUARE_WEIGHTS = [
        0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
        0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
        0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
        0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
        0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
        0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
        0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
        0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
        0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
        0,   0,   0,   0,   0,   0,   0,   0,   0,   0]
        opp = MIN
        score = 0
        for i in range(100):
            if board[i] == MAX:
                score += SQUARE_WEIGHTS[i]
            elif board[i] == opp:
                score -= SQUARE_WEIGHTS[i]
        return score

    def get_nodes(self):
        return nodes

    def terminal_test(self, player, board):
        opponent = self.opponent(player)
        if self.any_legal_move(player, board) or self.any_legal_move(opponent, board):
            return False
        return True

    def terminal_value(self, board):
        s = self.score(MAX, board)
        if s > 0:
            return 30000000
        elif s < 0:
            return -30000000
        else:
            return 0

    def minimax_strategy(self, max_depth):
        """ Takes a max_depth parameter and returns a new function/closure for strategy """
        def strategy(board, player):
            return self.alpha_beta(board, player, max_depth)
        return strategy

    def minimax(self, board, player, max_d):
        """ Takes a current board and player and max_depth and returns a best move
        This is the top level mini-max function. Note depth is ignored. We
        always search to the end of the game."""
        current_d = 0
        if player == MAX:
            move= self.max_dfs(board, player, max_d, 0)[1]
        if player == MIN:
            move= self.min_dfs(board, player, max_d, 0)[1]
        #print("player %s selects %i" % (player,move))
        return move

    def max_dfs(self, board, player, max_d, current_d, alpha, beta):
        global d
        if player == None:
            return self.terminal_value(board), None
        if current_d == max_d:
            return self.eval(board), None
        v = -10000
        move = 1
        for m in self.legal_moves(player,board):
            new_board = self.make_move(m, player, board*1)
            if (str(new_board),player) in d:
                v = d[(str(new_board), player)]
            else:
                v = self.eval(board)
                d.update({(str(new_board), player): v})
            v = max(v, self.min_dfs(new_board, self.next_player(board, player), max_d, current_d+1, alpha, beta)[0])
            if v >= beta:
                return v, move
            alpha = max(alpha, v)
            if alpha == v:
                move = m
        return v, move

    def min_dfs(self, board, player, max_d, current_d, alpha, beta):
        global d
        if player == None:
            return self.terminal_value(board), None
        if current_d == max_d:
            return self.eval(board), None
        v = 10000
        move = -1
        for m in self.legal_moves(player,board):
            new_board = self.make_move(m, player, board*1)
            if (str(new_board),player) in d:
                v = d[(str(new_board), player)]
            else:
                v = self.eval(board)
                d.update({(str(new_board), player): v})
            v = min(v, self.max_dfs(new_board, self.next_player(board, player), max_d, current_d+1, alpha, beta)[0])
            if v <= alpha:
                return v, move
            beta = min(beta, v)
            if beta == v:
                move = m
        return v, move

    def alpha_beta(self, board, player, max_d):
        if player == MAX:
            move= self.max_dfs(board, player, max_d, 0, -100000, 100000)[1]
        if player == MIN:
            move= self.min_dfs(board, player, max_d, 0, -100000, 100000)[1]
        #print("player %s selects %i" % (player,move))
        return move

    def best_strategy(self, board, player, best_move, still_running):
        i = 3
        while(still_running.value > 0 and best_move.value<1000):
            best_move.value  = self.alpha_beta(board, player, i)
            i = i+1








