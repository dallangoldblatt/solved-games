
from typing import Any, Dict, List

from games import Game, GameState


class TTTGameState(GameState):
    """
    Representation of a specific board state.
    player: the player that played last_move
    board: the current board state
    board_size: the number of spaces per row (and col)
    last_move: the index of the last move made by player
    """

    def __init__(self, player: int, board: Any, board_values: Dict[Any, float],
                 last_move: int, kwargs: Dict[str, Any] = None):
        super().__init__(player, board, board_values, last_move, kwargs=kwargs)
        if last_move == -1:
            return

        # Determine if the game has ended
        # Enumerate the indices of the possible winning lines
        board_size = kwargs['board_size']
        row, col = divmod(last_move, board_size)
        winning_lines = []
        # Add row of last_move
        winning_lines.append(list(range(board_size * row, board_size * (row + 1))))
        # Add col of last_move
        winning_lines.append(list(range(col, col + board_size ** 2, board_size)))
        # Add top left to bottom right diagonal
        if row == col:
            winning_lines.append(list(range(0, board_size ** 2, board_size + 1)))
        # Add top right to bottom left diagonal
        if row + col == board_size - 1:
            winning_lines.append(list(range(board_size - 1, board_size ** 2 - 1, board_size - 1)))

        # Check if last move ended the game
        self.win = any([all(self.board[index] == self.player for index in line) for line in winning_lines])
        self.tie = not self.win and all([space != GameState.EMPTY for space in self.board])
        self.ended = self.win or self.tie


class TTTGame(Game):
    # Player markers
    FIRST = 'X'
    SECOND = 'O'

    gamestate_cls = TTTGameState

    def __init__(self, player_first: bool, board_size: int = 3):
        self.board = [GameState.EMPTY] * (board_size ** 2)
        self.board_size = board_size

        self.kwargs = {'board_size': board_size}
        super().__init__(player_first)

    def player_turn(self, move):
        self.take_turn(move, False)

    def ai_turn(self):
        # Update player about board state
        self.print_board()
        print('My turn! Thinking...')

        # Find best move for AI in this state
        this_state = TTTGameState(GameState.PLAYER, self.board, self.board_values, -1, self.kwargs)
        ai_move = this_state.get_best_move()

        self.take_turn(ai_move, True)

    def print_board(self, print_indices=True):
        """ Print the game board. For a 3x3 game the output should be:

           | X |  	  0 | 1 | 2
         ---------	  ---------
           | O |  	  3 | 4 | 5
         ---------	  ---------
         X |   |  	  6 | 7 | 8

        """
        print()
        board_size = self.board_size

        # Get the text that will be in each space
        tokens = [self.markers[space] for space in self.board]
        indices = list(range(self.board_size**2))

        # Chop list into board_size length lists
        newline_indices = list(range(0, board_size**2, board_size))
        token_lines = [tokens[i:i+board_size] for i in newline_indices]
        index_lines = [indices[i:i+board_size] for i in newline_indices]

        # Join inner lists to create each line
        token_lines = [' | '.join(tokens) for tokens in token_lines]
        if board_size == 3:
            index_lines = [' | '.join(map(str, indices)) for indices in index_lines]
        else:
            index_lines = [' | '.join(map(lambda x: str(x).rjust(2), indices)) for indices in index_lines]

        # Create horizontal line to go between lines
        horiz_line = '-' * (3 * (board_size - 1) + board_size)

        # Print board and indices together
        if print_indices:
            for i in range(board_size - 1):
                print(' ' + token_lines[i] + '    ' + index_lines[i])
                if board_size == 3:
                    print(' ' + horiz_line + '    ' + horiz_line)
                else:
                    print(' ' + horiz_line + '    ' + horiz_line + '----')
            print(' ' + token_lines[-1] + '    ' + index_lines[-1])
            print()
        else:
            for i in range(board_size - 1):
                print(' ' + token_lines[i] )
                print(' ' + horiz_line )
            print(' ' + token_lines[-1])
            print()
