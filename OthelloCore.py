"""
Base class for Othello Core
Must be subclassed by student Othello solutions
"""

#

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

class OthelloCore:
    def squares(self):
        """List all the valid squares on the board."""
        return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


    def initial_board(self):
        """Create a new board with the initial black and white positions filled."""
        board = [OUTER] * 100
        for i in self.squares():
            board[i] = EMPTY
        # The middle four squares should hold the initial piece positions.
        board[44], board[45] = WHITE, BLACK
        board[54], board[55] = BLACK, WHITE
        return board


    def print_board(self,board):
        """Get a string representation of the board."""
        rep = ''
        rep += '  %s\n' % ' '.join(map(str, list(range(1, 9))))
        for row in range(1, 9):
            begin, end = 10 * row + 1, 10 * row + 9
            rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
        return rep


    def is_valid(self, move):
        """Is move a square on the board?"""
        return move in self.squares()

    def opponent(self, player):
        """Get player's opponent piece."""
        if player == PLAYERS[WHITE]:
            opp = PLAYERS[BLACK]
        else:
            opp = PLAYERS[WHITE]
        return opp

    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        Returns the index of the bracketing square if found
        """
        if player == PLAYERS[BLACK]:
            symb = WHITE
            opp = BLACK
        else:
            symb = BLACK
            opp = WHITE
        s = square
        s = s + direction
        if board[s] == symb:
            while board[s] == symb:
                s = s + direction
            if board[s] == opp:
                return s
        return None
    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        moves = []
        if board[move] == EMPTY:
            for direction in DIRECTIONS:
                m = self.find_bracket(move, player, board, direction)
                if m is not None:
                    moves.append(move)
        if len(moves) is not 0:
            return True
        return False

    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    def make_move(self, move, player, board):
        """Update the board to reflect the move by the specified player."""
        if player == PLAYERS[BLACK]:
            symb = BLACK
        else:
            symb = WHITE
        if self.is_legal(move, player, board):
            board[move]= symb
            b = board[:]
            for direction in DIRECTIONS:
                b = self.make_flips(move, player, b, direction)[:]
            return b
        return None
    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        if player == PLAYERS[BLACK]:
            symb = BLACK
        else:
            symb = WHITE
        m = self.find_bracket(move, player, board, direction)
        if m is not None:
            s = move + direction
            while s is not m:
                board[s] = symb
                s = s+direction
        return board
    def legal_moves(self, player, board):
        """Get a list of all legal moves for player, as a list of integers"""
        moves = []
        for i in range(100):
            if self.is_legal(i, player, board):
                moves.append(i)
        return moves
    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
        if len(self.legal_moves(player, board)) == 0:
            return False
        return True

    def next_player(self,board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        player = self.opponent(prev_player)
        if self.any_legal_move(player, board):
            return player
        elif self.any_legal_move(prev_player, board):
            return prev_player
        return None

    def score(self,player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        w = board.count(WHITE)
        b = board.count(BLACK)
        if player == PLAYERS[WHITE]:
            return w-b
        else:
            return b-w

class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)
