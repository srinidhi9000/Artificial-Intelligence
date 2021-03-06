#SRINIDHI KRISHNAN
from core import *
import math
import random
d = {}
def minimax_strategy(max_depth):
        """ Takes a max_depth parameter and returns a new function/closure for strategy """
        def strategy(board, player):
            return minimax(board, player, max_depth)
        return strategy

def minimax(board, player, max_depth):
    """ Takes a current board and player and max_depth and returns a best move
    This is the top level mini-max function. Note depth is ignored. We
    always search to the end of the game."""
    current_d = 0
    if player == MAX:
        move= max_dfs(board, player, max_depth, current_d)[1]
    if player == MIN:
        move= min_dfs(board, player, max_depth, current_d)[1]
    #print("player %s selects %i" % (player,move))
    return move

def max_dfs(board, player, max_d, current_d):
    global d
    if terminal_test(board):
        return terminal_value(terminal_test(board)), None
    v = -10000
    move = 1
    for m in actions(board):
        new_board = result(board,player,m)
        if terminal_value(new_board) == 1:
            break
        if (new_board,player) in d:
            new_value = d[(new_board, player)]
        else:
            new_value = min_dfs(make_move(board, player, m), toggle(player), max_d, current_d+1)[0]
            d.update({(new_board,player): new_value})
        if new_value == 1:
            return new_value, m
        if new_value > v:
            v = new_value
            move = m
    return v, move

def terminal_value(val):
    if val == "X":
        return 1
    elif val == "O":
        return -1
    return 0

def min_dfs(board, player, max_d, current_d):
    global d
    if terminal_test(board):
        return terminal_value(terminal_test(board)), None
    move = -1
    v = 10000
    for m in actions(board):
        new_board = result(board,player,m)
        if terminal_value(new_board) == -1:
            break
        if (new_board,player) in d:
            new_value = d[(new_board, player)]
        else:
            new_value = max_dfs(make_move(board, player, m), toggle(player), max_d, current_d+1)[0]
            d.update({(new_board,player): new_value})
        if new_value == -1:
            return new_value, m
        if new_value < v:
            v = new_value
            move = m
    return v, move

def human(board, player):
    l = actions(board)
    rand = random.randint(0, len(l)-1)
    return int(l[rand])


