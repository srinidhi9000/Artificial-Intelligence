import random
board = [0,0,0,0,0,0,0,0,0]
done =0

def post_move(r,c):
    i = r*3 +c
    board[i] = 1

def get_move():
    while True:
        i = random.randint(0, 8)
        if board[i] == 0:
            board[i] = -1
            return i

def display():
    s = ""
    for i in range(9):
        s += str(board[i])
        s += " "
        if i % 3 == 2:
                s += "\n"
    return s


def goal_test():
    for i in range(0,3):
        if board[i*3] == board[i*3+1] == board[i*3+2]:
            if board[i*3] == 1:
                print("player wins")
            elif board[i*3] == 0:
                return False
            else:
                print("computer wins")
            return True
        elif board[i] == board[i+3] == board[i+6]:
            if board[i] == 1:
                print("player wins")
            elif board[i] == 0:
                return False
            else:
                print("computer wins")
            return True
    if board[0] == board[4] == board[8]:
        if board[0] == 1:
            print("player wins")
        elif board[0] == 0:
                return False
        else:
            print("computer wins")
        return True
    if board[2] == board[4] == board[6]:
        if board[2] == 1:
            print("player wins")
        elif board[2] == 0:
                return False
        else:
            print("computer wins")
        return True
    for x in board:
        if x == 0:
            return False
    print("tie")
    return True

def client():
     print("You are 1, computer is -1")
     while True:
        row = input("Enter row (0-2): ")
        col = input("Enter col (0-2): ")
        post_move(int(row),int(col))
        if goal_test():
            return
        get_move()
        print(display())
        if goal_test():
            return

if __name__ == "__main__":
    client()
