from core import *
import random
import math

def minimax_strategy(max_depth):
        """ Takes a max_depth parameter and returns a new function/closure for strategy """
        def strategy(board, player):
            return minimax(board, player, max_depth)
        return strategy


def minimax(board, player, max_depth):
        """ Takes a current board and player and max_depth and returns a best move
         This is the top level mini-max function. Note depth is ignored. We
         always search to the end of the game."""
        if player == MAX: move= max_dfs(board, player, max_depth,9)[1]
        if player == MIN: move= min_dfs(board, player, max_depth,9)[1]
        #print("player %s selects %i" % (player,move))
        return move

def eval_terminal(val):
    if val is "X":
        return 1
    if val is "O":
        return -1
    if val is "TIE":
        return 0

def max_dfs(board, player, max_d, current_d):
    if terminal_test(board):
        return eval_terminal(terminal_test(board)), None
    v = -math.inf
    move = -1
    for m in actions(board):
        new_value = min_dfs(make_move(board, player, m), toggle(player), max_d, current_d+1)[0]
        if int(new_value) > v:
            v = new_value
            move = m
    return move, v

def min_dfs(board, player, min_d, current_d):
    if terminal_test(board):
        return eval_terminal(terminal_test(board)), None
    v = math.inf
    move = -1
    for m in actions(board):
        new_value = max_dfs(make_move(board, player, m), toggle(player), min_d, current_d+1)[0]
        if int(new_value) < v:
            v = new_value
            move = m
    return move, v


def human(board, player):
    list = actions(board)
    rand = random.randint(0, len(list)-1)
    return int(list[rand])
