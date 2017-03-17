terminal_count = 0
all_boards = []
count = 0

def gt(board):
    for i in range(0, 3):
        sum = board[i * 3] + board[i * 3 + 1] + board[i * 3 + 2]
        if sum == 3 or sum == -3:
            return True
        s2 = board[i] + board[i + 3] + board[i + 6]
        if s2 == 3 or s2 == -3:
            return True
    s3 = board[0] + board[4] + board[8]
    if s3 == 3 or s3 == -3:
        return True
    s4 = board[2] + board[4] + board[6]
    if s4 == 3 or s4 == -3:
        return True
    for x in board:
        if x == 0:
            return False
    return True

def actions(board):
    n = []
    for i in range(9):
        if board[i] == 0:
            n.append(i)
    return n

def result(board, player, act):
    l = list(board)
    l[act] = player
    if player == -1:
        player = 1
    else:
        player = -1
    return l, player

def dfs(board,player,depth):
    global count, terminal_count, all_boards
    if depth>4 and gt(board):
        terminal_count += 1
        all_boards.append(board)
        return None
    for a in actions(board):
        board, player = result(board, player, a)
        dfs(board,player, depth +1)
        count += 1

"""def dfs():
    global done
    global turn
    global zero_count
    fringe = []
    a = set()
    # add in empty board
    fringe.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    while True:
        print(done)
        if len(fringe) == 0:
            print(done)
            return
        board = fringe.pop(0)
        if gt(board):
            done += 1
            a.add(str(board))
        else:
            for i in range(9):
                if board[i] == 0:
                    zero_count += 1
            if zero_count % 2 == 0:
                turn = -1
            else:
                turn = 1
            for i in range(9):
                if board[i] == 0:
                    nl = list(board)
                    nl[i] = turn
                    fringe.append(nl)"""


if __name__ == "__main__":
    dfs([0,0,0,0,0,0,0,0,0], -1, 0)
    print(terminal_count)
    print(count)
    print(gt([-1,1,-1,1,-1,1,-1,0,0]))
