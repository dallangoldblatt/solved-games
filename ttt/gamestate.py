class GameState():
    """
    The game board is a list with 9 indices:

    0 | 1 | 2 => [0, 1, 2, 3, 4, 5, 6, 7, 8]
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """


    def __init__(self, max_turn, board, move):
        self.max_turn = max_turn
        self.board = board
        self.move = move

        # Apply move to board
        self.board[move] = max_turn

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
        # Check if move ended the game
        self.win = all([self.board[index] == max_turn for line in winning_lines[self.move] for index in line])
        self.tie = not self.win and all([space != -1 for space in self.board])
        self.ended = self.win or self.tie

    def get_utility(self):
        if not self.ended:
            # Consider all possible next gamestates
            for index, space in enumerate(board):
                if space != -1:
                    continue
                # TODO

        elif self.tie:
            # Neither player wins:
            return 0
        elif self.win and max_turn:
            # Max player wins
            return 1
        else:
            # Min player wins
            return -1
