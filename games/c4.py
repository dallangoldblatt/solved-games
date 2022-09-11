
import random
from typing import Any, Dict, Generator, List, Tuple

from games import Game, GameState


class C4GameState(GameState):
    """
    Representation of a specific board state.
    player: the player that played last_move
    board: the current board state
    board_size: the number of spaces per row (and col)
    last_move: the index of the last move made by player
    """

    # Map containing the index changes for travelling in each direction
    direction_step_map = {
        0: 1,
        1: -6,
        2: -7,
        3: -8,
        4: -1,
        5: 6,
        6: 7,
        7: 8
    }

    # Map from each axis (positive direction) to the list of possible start indices
    axis_start_map = {
        0: {0, 7, 14, 21, 28, 35},
        1: {21, 28, 35, 36, 37, 38},
        2: {35, 36, 37, 38, 39, 40, 41},
        3: {27, 34, 41, 40, 39, 38}
    }

    def check_win(self) -> bool:
        """Check if player's last move at index ends the game.

        Directions:
            3  2  1
             \ | /
           4 - i - 0
             / | \\
            5  6  7
        """
        board, player, index = self.board, self.player, self.last_move
        # Track which directions can still be expanded
        active = {dir: (True, index) for dir in self.direction_step_map}
        # Track the current length along each direction axis
        lengths = {axis: 1 for axis in range(0, 4)}
        # Count number of inactive directions
        inactive = 0

        while inactive < 8:
            for direction, step in self.direction_step_map.items():
                dir_active, dir_index = active[direction]
                if not dir_active:
                    # Skip inactive direction
                    continue

                # Step to next index in current direction
                prev_c, prev_r = dir_index % 7, dir_index // 7
                dir_index += step
                c, r = dir_index % 7, dir_index // 7

                try:
                    if abs(r - prev_r) > 1 or abs(c - prev_c) > 1:
                        # Index wrapped around board
                        raise IndexError
                    elif not (0 <= dir_index < len(board)):
                        # Index extends off of board
                        raise IndexError
                    elif board[dir_index] != player:
                        # Current index matches other player
                        raise ValueError
                    else:
                        # Increase length along axis and store index for next loop
                        lengths[direction % 4] += 1
                        dir_active = True
                except (IndexError, ValueError):
                    # Mark direction as inactive
                    inactive += 1
                    dir_active = False
                active[direction] = (dir_active, dir_index)

        return any(length >= 4 for length in lengths.values())


    def count_threes(self) -> Tuple[int, int]:
        """Count the number of potential wins for (player, other).
        """
        board, player = self.board, self.player

        # Track location of last empty index
        # If a potential four is found, it is the only empty space remaining
        empty_index = -1
        # Track set of empty indices that could be part of a four for each player
        player_counted, other_counted = set(), set()
        for axis, starts in self.axis_start_map.items():
            step = self.direction_step_map[axis]
            for start in starts:
                # Count how many player pieces are in the first window of four spaces
                num_player, num_other = 0, 0
                end = start + 3 * step
                for index in range(4):
                    piece = board[start + index * step]
                    if piece == player:
                        num_player += 1
                    elif piece == GameState.EMPTY:
                        empty_index = index
                    else:
                        num_other += 1

                while True:
                    # Check if current window could have a winning line for the player
                    if num_other == 0 and num_player == 3:
                        # New position where player could win
                        player_counted.add(empty_index)
                    elif num_other == 3 and num_player == 0:
                        # New position where other could win
                        other_counted.add(empty_index)

                    # Remove count for old item in window
                    old_piece = board[start]
                    if old_piece == player:
                        num_player -= 1
                    elif old_piece != GameState.EMPTY:
                        num_other -= 1

                    # Advance the window by one space
                    prev_c, prev_r = end % 7, end // 7
                    start += step
                    end += step
                    c, r = end % 7, end // 7
                    if abs(r - prev_r) > 1 or abs(c - prev_c) > 1:
                        # Window wrapped around board
                        break
                    elif not (0 <= end < len(board)):
                        # Window extends off of board
                        break

                    # Add count for new item in window
                    new_piece = board[end]
                    if new_piece == player:
                        num_player += 1
                    elif new_piece == GameState.EMPTY:
                        empty_index = end
                    else:
                        num_other += 1
        return len(player_counted), len(other_counted)

    def __init__(self, player: int, board: Any, board_values: Dict[Any, float],
                 last_move: int, kwargs: Dict[str, Any] = None):
        super().__init__(player, board, board_values, last_move, kwargs=kwargs)
        if last_move == -1:
            return

         # Check if last move ended the game
        self.win = self.check_win()
        self.tie = not self.win and all(space != GameState.EMPTY for space in self.board[:7])
        self.ended = self.win or self.tie

    def gen_indices(self) -> Generator[int, None, None]:
        """Generator of valid moves for AI.
        """
        # Try each column
        for index in random.sample(range(7), 7):
            if self.board[index] != GameState.EMPTY:
                # Column is full
                continue

            # Drop move down until no empty space
            try:
                while self.board[index + 7] == GameState.EMPTY:
                    index += 7
            except IndexError:
                pass
            yield index

    def heuristic(self) -> float:
        """Approximate value of non-terminal state.
        """
        # Count number of ways each player could win from here
        player_threes, other_threes = self.count_threes()

        # Convert difference in ways to number between -1 and 1
        # There are less than 50 spaces that could win the game
        # We only care about ordering
        h = (player_threes - other_threes) / 50
        if self.player == self.AI:
            return h
        else:
            return -h


class C4Game(Game):
    # Player markers
    FIRST = 'X'
    SECOND = 'O'

    gamestate_cls = C4GameState

    def __init__(self, player_first: bool, max_depth: int = 5, **kwargs):
        # The normal Connect 4 has 6 rows and 7 columns
        self.board = [GameState.EMPTY] * (6 * 7)
        self.gamestate_cls.max_depth = max_depth

        super().__init__(player_first)

    def move_is_valid(self, move: int) -> bool:
        """Check that move choice is valid.
        """
        return self.board[move - 1] == GameState.EMPTY

    def move_to_index(self, move: int) -> int:
        """Convert move choice to index in self.board
        """
        # Subtract one for index at top of column
        index = move - 1

        # Drop move down until no empty space
        try:
            while self.board[index + 7] == GameState.EMPTY:
                index += 7
        except IndexError:
            pass
        return index

    def print_board(self, print_indices=True):
        """ Print the game board. For a 3x3 game the output should be:

           |   |   |   |   |   |
           |   |   |   |   |   |
           |   |   |   |   |   |
           | O |   |   |   |   |
           | X | X |   |   |   |
           | X | O | O | X |   |
        ---------------------------
         1   2   3   4   5   6   7


           | X |  	  0 | 1 | 2
         ---------	  ---------
           | O |  	  3 | 4 | 5
         ---------	  ---------
         X |   |  	  6 | 7 | 8

        """

        # Get the text that will be in each space
        tokens = [self.markers[space] for space in self.board]

        # Print rows
        print()
        for i in range(0, len(self.board), 7):
            print(' ' + ' | '.join(tokens[i:i+7]))

        # Print guide
        print('---------------------------')
        print(' 1   2   3   4   5   6   7 ')
        print()
