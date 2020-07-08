from ttt.gamestate import GameState

class Game():

    def __init__(self, player_first, board_size=3):
        # An empty space is represented with -1
        self.board_size = board_size
        self.board = [-1] * (board_size ** 2)
        self.ended = False
        self.player_win = False

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

        # Check if the game has ended
        if not GameState(True, self.board, move).ended:
            self.ai_turn()
        else:
            self.ended = True
            self.player_win = True

    def ai_turn(self):
        # Update player about board state
        self.print_board()
        print('My turn! Thinking...')

        # Find best move for AI
        this_state = GameState(True, self.board, -1)
        ai_move = this_state.get_max_move()[0]

        # Set AI move
        self.board[ai_move] = False

        # Check if the game has ended
        if GameState(False, self.board, ai_move).ended:
            self.ended = True
            self.player_win = False

    def print_board(self):
        """ Print the game board. For a 3x3 game the output should be:

           | X |  	  0 | 1 | 2
         ---------	  ---------
           | O |  	  3 | 4 | 5
         ---------	  ---------
         X |   |  	  6 | 7 | 8

        """
        print()

        # Get the text that will be in each space
        tokens = [self.xo[space] for space in self.board]
        indices = list(range(self.board_size**2))

        # Chop list into self.board_size length lists
        newline_indices = list(range(0, self.board_size**2, self.board_size))
        token_lines = [tokens[i:i+self.board_size] for i in newline_indices]
        index_lines = [indices[i:i+self.board_size] for i in newline_indices]

        # Join inner lists to create each line
        token_lines = [' | '.join(tokens) for tokens in token_lines]
        index_lines = [' | '.join(map(str, indices)) for indices in index_lines]

        # Create horizontal line to go between lines
        horiz_line = '-' * (3 * (self.board_size - 1) + self.board_size)

        # Wrint board and indices together
        for i in range(self.board_size - 1):
            print(' ' + token_lines[i] + '\t' + index_lines[i])
            print(' ' + horiz_line + '\t' + horiz_line)
        print(' ' + token_lines[-1] + '\t' + index_lines[-1])
        print()
