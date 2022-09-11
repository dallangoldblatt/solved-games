
import random
from typing import Any, Dict, Generator, List

from games import Game, GameState


class TTTGameState(GameState):
    """
    Representation of a specific board state.
    player: the player that played last_move
    board: the current board state
    board_size: the number of spaces per row (and col)
    last_move: the index of the last move made by player
    """

    max_depth = None

    def __init__(self, player: int, board: Any, board_values: Dict[int, float],
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
        self.win = any(all(self.board[index] == self.player for index in line) for line in winning_lines)
        self.tie = not self.win and all(space != GameState.EMPTY for space in self.board)
        self.ended = self.win or self.tie

    def gen_indices(self) -> Generator[int, None, None]:
        """Generator of valid move indices for AI.
        """
        n = len(self.board)
        for index in random.sample(range(n), n):
            if self.board[index] == GameState.EMPTY:
                yield index

class TTTGame(Game):
    # Player markers
    FIRST = 'X'
    SECOND = 'O'

    gamestate_cls = TTTGameState

    def __init__(self, player_first: bool, board_size: int = 3, **kwargs):
        self.board = [GameState.EMPTY] * (board_size ** 2)
        self.board_size = board_size
        self.gamestate_cls.max_depth = max_depth

        self.kwargs = {'board_size': board_size}
        super().__init__(player_first)

    def move_is_valid(self, move: int) -> bool:
        """Check that move choice is valid.
        """
        return 1 <= move <= 9

    def move_to_index(self, move: int) -> int:
        """Convert move choice to index in self.board
        """
        return move - 1

    def print_board(self, print_indices=True):
        """ Print the game board. For a 3x3 game the output should be:

           | X |  	  1 | 2 | 3
         ---------	  ---------
           | O |  	  4 | 5 | 6
         ---------	  ---------
         X |   |  	  7 | 8 | 9

        """
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
            index_lines = [' | '.join(map(lambda x: str(x+1), indices)) for indices in index_lines]
        else:
            index_lines = [' | '.join(map(lambda x: str(x+1).rjust(2), indices)) for indices in index_lines]

        # Create horizontal line to go between lines
        horiz_line = '-' * (3 * (board_size - 1) + board_size)

        # Print board and indices together
        print()
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
