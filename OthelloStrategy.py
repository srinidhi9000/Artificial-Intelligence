import OthelloCore as core
import random
c = core.OthelloCore()
def random_strategy(player,board):
    moves = c.legal_moves(player, board)
    if len(moves) is not 0:
        pick = random.choice(moves)
        board = c.make_move(pick, player, board).copy()
    return board
MAX = "Black"
MIN = "White"
INF = 10000
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
def eval(board, player):
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
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    symb = BLACK
    score = 0
    for i in range(100):
        if board[i] == symb:
            score = score + SQUARE_WEIGHTS[i]
    return score
def max_dfs(board, player, max_d, current_d):
    t = terminal_test(board, player)
    if t is not False:
        return terminal_value(board, t), None
    if current_d == max_d:
        return eval(board, player), None
    v = -INF
    move = -1
    for m in c.legal_moves(player, board):
        new_value = min_dfs(c.make_move(m, player, board), c.next_player(board, player), max_d, current_d+1)[0]
        if new_value > v:
            v = new_value
            move = m
    return (v, move)
def min_dfs(board, player, max_d, current_d):
    t = terminal_test(board, player)
    if t is not False:
        return terminal_value(board, t), None
    if current_d == max_d:
        return eval(board, player), None
    v = INF
    move = -1
    for m in c.legal_moves(player, board):
        new_value2 = max_dfs(c.make_move(m, player, board), c.next_player(board, player), max_d, current_d+1)[0]
        if new_value2 < v:
            v = new_value2
            move = m
    return (v, move)
def minimax(player, board, max_d):
    if player == MAX:
        return max_dfs(board, player, max_d, 0)[1]
    if player == MIN:
        return min_dfs(board, player, max_d, 0)[1]
def minimax_strategy(max_depth):
    """ Takes a max_depth parameter and returns a new function/closure for strategy """
    def strategy(player, board):
        b = board[:]
        move = minimax(player, board, max_depth)
        return c.make_move(move, player, b)
    return strategy
def terminal_value(board, winner):
    if winner == MAX:
        return 10000000
    elif winner == MIN:
        return -10000000
    else:
        return 0
def terminal_test(board,player):
    if c.any_legal_move(player, board):
        return False
    if c.any_legal_move(c.opponent(player), board):
        return False
    return True
