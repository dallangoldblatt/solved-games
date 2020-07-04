class GameState():
    """
    The game board is a list with 9 indices:

    0 | 1 | 2 => [0, 1, 2, 3, 4, 5, 6, 7, 8]
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """

    def __init__(self, max_turn, board, last_move):
        self.max_turn = max_turn
        self.board = board.copy()
        self.last_move = last_move

        # Matches a move to the possible lines that it could complete
        winning_lines =
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
        self.win = any([self.board[index] == max_turn for line in winning_lines[self.last_move] for index in line]) # TODO any all
        self.tie = not self.win and all([space != -1 for space in self.board])
        self.ended = self.win or self.tie

    def get_max_move(self):
        # Max seeks to maximize move utility
        best_move, best_value = -1, -2
        for index, space in enumerate(self.board):
            if space != -1:
                continue
            next_state = GameState(not max_turn, self.board, index)
            next_value = next_state.get_utility()
            if next_value > best_value:
                best_move = index
                best_value = next_value
        return (best_move, best_value)

    def get_min_move(self):
        # Min seeks to maximize move utility
        best_move, best_value = -1, 2
        for index, space in enumerate(self.board):
            if space != -1:
                continue
            next_state = GameState(not max_turn, self.board, index)
            next_value = next_state.get_utility()
            if next_value < best_value:
                best_move = index
                best_value = next_value
        return (best_move, best_value)

    def get_utility(self):
        if not self.ended:
            # Consider all possible next gamestates
            if max_turn:
                return get_max_move()[1]
            else:
                return get_min_move()[1]
        elif self.tie:
            # Neither player wins
            return 0
        elif max_turn:
            # AI wins
            return 1
        else:
            # Player wins
            return -1
