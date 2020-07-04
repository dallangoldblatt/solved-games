from ttt.gamestate import GameState

class Game():

    def __init__(self, player_first):
        # An empty space is represented with -1
        self.board = [-1] * 9
        self.ended = False

        # X goes first
        # Map player to X or O
        if player_first:
            self.xo = {True:'X', False:'O', -1:' '}
        else:
            self.xo = {True:'O', False:'X', -1:' '}

        # If the player lost the coin toss, let the AI move first
        if not player_first:
            self.ai_turn()

    def player_turn(self, move):

        # Set player move
        self.board[move] = True

        self.print_board()

        # Check if the game has ended
        if not GameState(True, self.board, move).ended:
            self.ai_turn()
        else:
            self.ended = True

    def ai_turn(self):
        print()
        print('My turn! Thinking...')

        # Find best move for AI
        this_state = GameState(True, self.board, -1)
        ai_move = this_state.get_max_move()[0]

        # Set AI move
        self.board[ai_move] = False

        # Check if the game has ended
        if GameState(False, self.board, ai_move).ended:
            self.ended = True

        self.print_board()

    def print_board(self):
        """
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
        """
        # TODO fix this to remake board list as x and o
        print(f' {self.xo[self.board[0]]} | {self.xo[self.board[1]]} | {self.xo[self.board[2]]}          0 | 1 | 2')
        print(f' ---------          ---------')
        print(f' {self.xo[self.board[3]]} | {self.xo[self.board[4]]} | {self.xo[self.board[5]]}          3 | 4 | 5')
        print(f' ---------          ---------')
        print(f' {self.xo[self.board[6]]} | {self.xo[self.board[7]]} | {self.xo[self.board[8]]}          6 | 7 | 8')
