from strategy import Strategy, BLACK,WHITE
from OthelloStrategy5_padusuma import OthelloStrategy
ai = Strategy()
ai2 = OthelloStrategy()

from Othello_Core import *
core = OthelloCore()

import random
import time
#############################################################
# client.py
# a simple othello client
# plays 2 strategies against each other and keeps score
# imports strategies from "strategies.py" as ai
# rest of functionality is stored in core.py
#
# SRINIDHI KRISHNAN
############################################################

B_STRATEGY = ai.human_strategy()
W_STRATEGY = ai.minimax_strategy(6)
ROUNDS = 10
SILENT = False

# see core.py for constants: MAX, MIN, TIE

def play(strategy_b, strategy_w, first=BLACK, silent=True):
    """
    Plays strategy_b vs. strategy_w, beginning with first
    in one game. Returns score as a result (string)

    The functions make_move, next_player and terminal_test are
    implemented elsewhere (e.g. in core.py). The current implementation
    uses a 9-char string as the state, but that is not exposed at this level.
    """
    board = core.initial_board()
    print(core.print_board(board))
    player = first
    current_strategy = {BLACK: strategy_b, WHITE: strategy_w}
    while player is not None:
        move = current_strategy[player](board, player)
        board = ai.make_move(move, player, board)
        player = ai.next_player(board, player)
        if not silent: print(core.print_board(board))
    return ai.count(board)


def main():
    """
    Plays ROUNDS othello games and keeps a count of
    wins/ties. Uses strategies defined as global constants above.
    Selects a random starting player
    """
    j =[]
    bl = wh =0
    for i in range(ROUNDS):
        try:
            start = time.time()
            game_result = play(B_STRATEGY, W_STRATEGY,
                          first=random.choice([BLACK, WHITE]),
                          silent=SILENT)
            j=game_result
            end = time.time()
            dur = end-start
            print(dur)
            #print("Winner: ", game_result)
        except core.IllegalMoveError as e:
            print(e)
        b =j[0]
        w =j[1]
        print("B: "+str(b))
        print("W: "+str(w))
        if(b==w):
            print("Tie!")
        elif(b>w):
            print("Black Wins!")
            bl+=1
        else:
            print("White Wins!")
            wh+=1
    print(str(bl) + " " + str(wh))



if __name__ == "__main__":
    main()
