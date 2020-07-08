class GameState():
    """
    The game board is a list with 9 indices:

    0 | 1 | 2 => [0, 1, 2, 3, 4, 5, 6, 7, 8]
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """

    def __init__(self, player, board, last_move):
        self.player = player
        self.board = board.copy()
        self.last_move = last_move

        self.EMPTY = -1

        # Skip first move:
        if last_move == -1:
            self.ended = False
            return

        # Apply move
        self.board[last_move] = self.player

        # Matches a move to the possible lines that it could complete
        winning_lines = \
        {
            0: [[0, 1, 2], [0, 4, 8], [0, 3, 6]],
            1: [[0, 1, 2], [1, 4, 7]],
            2: [[0, 1, 2], [2, 4, 6], [2, 5, 8]],
            3: [[0, 3, 6], [3, 4, 5]],
            4: [[0, 4, 8], [1, 4, 7], [2, 4, 6], [3, 4, 5]],
            5: [[2, 5, 8], [3, 4, 5]],
            6: [[0, 3, 6], [2, 4, 6], [6, 7, 8]],
            7: [[1, 4, 7], [6, 7, 8]],
            8: [[0, 4, 8] ,[2, 5, 8], [6, 7, 8]]
        }

        # Check if last move ended the game
        self.win = any([all(self.board[index] == self.player for index in line) for line in winning_lines[self.last_move]])
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
                # Update with value of next state
                next_state = GameState(not state.player, state.board, index)
                next_value = next_state._get_best_move(next_state, alpha, beta)[1]
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
                # Update with value of next state
                next_state = GameState(not state.player, state.board, index)
                next_value = next_state._get_best_move(next_state, alpha, beta)[1]
                if next_value < best_value:
                    best_move, best_value = index, next_value
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        # Prune
                        break
            return (best_move, best_value)
