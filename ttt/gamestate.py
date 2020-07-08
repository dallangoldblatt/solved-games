class GameState():
    """
    Represntation of a specific board state.
    player: the player that played last_move
    board: the current board state
    board_size: the number of spaces per row (and col)
    last_move: the index of the last move made by player
    """

    def __init__(self, player, board, board_size, board_values, last_move):
        self.player = player
        self.board = board.copy()
        self.board_size = board_size
        self.board_values = board_values
        self.last_move = last_move

        self.EMPTY = -1

        # Skip first move:
        if last_move == -1:
            self.ended = False
            return

        # Apply move
        self.board[last_move] = self.player

        # Enumerate the indices of the possible winning lines
        row, col = divmod(last_move, board_size)
        winning_lines = []
        # Add rows
        winning_lines.append(list(range(board_size * row, board_size * (row + 1))))
        # Add cols
        winning_lines.append(list(range(col, col + board_size ** 2, board_size)))
        # Add top left to bottom right diagonal
        if row == col:
            winning_lines.append(list(range(0, board_size ** 2, board_size + 1)))
        # Add top right to bottom left diagonal
        if row + col == board_size - 1:
            winning_lines.append(list(range(board_size - 1, board_size ** 2 - 1, board_size - 1)))

        # Check if last move ended the game
        self.win = any([all(self.board[index] == self.player for index in line) for line in winning_lines])
        self.tie = not self.win and all([space != self.EMPTY for space in self.board])
        self.ended = self.win or self.tie

    def get_best_move(self):
        # Get the best move for the current player
        return self._get_best_move(self, -2, 2)[0]

    def _get_best_move(self, state, alpha, beta):
        # Recursive function for finding the best move in a state
        # Implements alpha-beta pruning
        if state.ended:
            # Terminal states are assigned a fixed-value
            if self.tie:
                # Neither player wins
                return (state.last_move, 0)
            elif not state.player:
                # AI wins
                return (state.last_move, 1)
            else:
                # Player wins
                return (state.last_move, -1)
        # Non-terminal states need to enumerate child states
        if state.player:
            best_move, best_value = -1, -2
            for index, space in enumerate(state.board):
                # Skip used spaces
                if space != self.EMPTY:
                    continue
                next_state = GameState(not state.player, state.board, self.board_size, self.board_values, index)
                try:
                    # Check if next state's value already has been calculated
                    key = tuple(next_state.board)
                    next_value = self.board_values[key]
                except KeyError:
                    # If not, save for future since tree traversal has overlapping nodes
                    next_value = next_state._get_best_move(next_state, alpha, beta)[1]
                    self.board_values[key] = next_value
                # Update best
                if next_value > best_value:
                    best_move, best_value = index, next_value
                    alpha = max(alpha, best_value)
                    if alpha >= beta:
                        # Prune
                        break
            return (best_move, best_value)
        else:
            best_move, best_value = -1, 2
            for index, space in enumerate(state.board):
                # Skip used spaces
                if space != self.EMPTY:
                    continue
                next_state = GameState(not state.player, state.board, self.board_size, self.board_values, index)
                try:
                    # Check if next state's value already has been calculated
                    key = tuple(next_state.board)
                    next_value = self.board_values[key]
                except KeyError:
                    # If not, save for future since tree traversal has overlapping nodes
                    next_value = next_state._get_best_move(next_state, alpha, beta)[1]
                    self.board_values[key] = next_value
                # Update best
                if next_value < best_value:
                    best_move, best_value = index, next_value
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        # Prune
                        break
            return (best_move, best_value)
