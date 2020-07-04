class Game():

    def __init__(self, player_first):
        # An empty space is represented with -1
        self.board = [-1] * 9

        # If the player lost the coin toss, let the AI move first
        if not player_first:
            ai_turn()


    def player_turn(self, move):
        # Set player move
        self.board[move] = True

        # Check if the game has ended
        if not GameState(False, self.board, move).ended:
            ai_turn()

    def ai_turn(self):
        print('Thinking...')

        # Find best move for AI
        next_state = GameState(True, self.board, move) # TODO fix move
        ai_move = next_state.get_max_move()[0]

        # Set AI move
        self.board[ai_move] = False

        print_board()

    def print_board(self):
        """
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
        """
        print(f' {self.board[0]} | {self.board[1]} | {self.board[2]}')
        print(f' ---------')
        print(f' {self.board[3]} | {self.board[4]} | {self.board[5]}')
        print(f' ---------')
        print(f' {self.board[6]} | {self.board[7]} | {self.board[8]}')
