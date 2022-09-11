
from typing import Any, Dict, Generator, List


class GameState():
    """
    Representation of a specific board state.
        player: the player (PLAYER or AI) that played last_move
        board: the current board state
        board_values: cache of known board values
        last_move: the index of the last move made by player
        kwargs: game-specific options
    """

    PLAYER: int = 1
    AI: int = -1
    EMPTY: int = 0

    player: int = None
    board: Any = None
    win: bool = False
    tie: bool = False
    ended: bool = False
    last_move: int = -1
    board_values: Dict[Any, float]


    def __init__(self, player: int, board: Any, board_values: Dict[int, float],
                 last_move: int = None, kwargs: Dict[str, Any] = None):
        self.player = player
        self.board = board.copy()
        self.board_values = board_values
        self.last_move = last_move
        self.kwargs = kwargs

        self.hash = hash((tuple(self.board), player))

        # Skip first move:
        if last_move == -1:
            self.ended = False
            return

        # Apply move
        self.board[last_move] = self.player

    def __hash__(self) -> int:
        return self.hash

    def gen_indices(self) -> Generator[int, None, None]:
        """Generator of valid moves for AI.
        """
        raise NotImplementedError

    def heuristic(self) -> float:
        """Approximate value of non-terminal state.
        """
        raise NotImplementedError

    def get_best_move(self) -> int:
        """Get the best move for the current player.
        """
        # Get the best move for the current player
        return self._get_best_move(self, -2, 2, 0)[0]

    def _get_best_move(self, state, alpha, beta, depth):
        """Recursive function for finding the best move in a state.
        Implements alpha-beta pruning.
        """
        if state.ended:
            # Terminal states are assigned a fixed-value
            if state.tie:
                # Neither player wins
                return (state.last_move, 0, False)
            elif state.player == self.AI:
                # AI wins
                return (state.last_move, 1, False)
            else:
                # Player wins
                return (state.last_move, -1, False)
        # Approximate value of non-terminal state at max_depth
        elif self.max_depth and depth == self.max_depth:
            return (state.last_move, state.heuristic(), True)
        # Non-terminal states need to enumerate child states
        elif state.player == self.PLAYER:
            best_move, best_value, best_approximated = -1, -2, None
            for index in self.gen_indices():
                next_state = type(state)(self.AI, state.board, self.board_values, index, self.kwargs)
                try:
                    # Check if next state's value already has been calculated
                    next_value = self.board_values[next_state]
                except KeyError:
                    # If not, save for future since tree traversal has overlapping nodes
                    _, next_value, approximated = next_state._get_best_move(next_state, alpha, beta, depth + 1)
                    if not approximated:
                        self.board_values[next_state] = next_value
                # Update best
                if next_value > best_value:
                    best_move, best_value, best_approximated = index, next_value, approximated
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    # Prune
                    break
            return (best_move, best_value, best_approximated)
        else:
            best_move, best_value, best_approximated = -1, 2, None
            for index in self.gen_indices():
                next_state = type(state)(self.PLAYER, state.board, self.board_values, index, self.kwargs)
                try:
                    # Check if next state's value already has been calculated
                    next_value = self.board_values[next_state]
                except KeyError:
                    # If not, save for future since tree traversal has overlapping nodes
                    _, next_value, approximated = next_state._get_best_move(next_state, alpha, beta, depth + 1)
                    if not approximated:
                        self.board_values[next_state] = next_value
                # Update best
                if next_value < best_value:
                    best_move, best_value, best_approximated = index, next_value, approximated
                beta = min(beta, best_value)
                if beta <= alpha:
                    # Prune
                    break
            return (best_move, best_value, best_approximated)


class Game():

    # Player markers
    FIRST: str = None
    SECOND: str = None

    # Game vars
    gamestate_cls: Any = None
    board: Any = None
    ended: bool = False
    result: str = ''
    board_values: Dict[Any, float] = {}
    kwargs: Dict[str, Any] = {}
    markers: Dict[int, str]

    def __init__(self, player_first: bool):
        # Create dictionary for remembering value of particular board states
        self.board_values = {}

        # Map player to correct marker
        if player_first:
            self.markers = {GameState.PLAYER: self.FIRST, GameState.AI: self.SECOND, GameState.EMPTY: ' '}
        else:
            self.markers = {GameState.PLAYER: self.SECOND, GameState.AI: self.FIRST, GameState.EMPTY: ' '}

        # If the player lost the coin toss, let the AI move first
        if not player_first:
            self.ai_turn()

    def handle_next_state(self, next_state: GameState, ai_turn: bool):
        """Check if the next state ends the game and update result.
        """
        if next_state.ended:
            # Indicate that the game has ended
            self.ended = True
            if next_state.tie:
                self.result = 'Tie game'
            elif ai_turn:
                self.result = 'You lose'
            else:
                self.result = 'You win!'

    def move_is_valid(cls, move: int) -> bool:
        """Check that move choice is valid.
        """
        raise NotImplementedError

    def move_to_index(cls, move: int) -> int:
        """Convert move choice to index in self.board
        """
        raise NotImplementedError

    def take_turn(self, move: int, ai_turn: bool):
        # Modify board with player's move
        marker = GameState.AI if ai_turn else GameState.PLAYER
        self.board[move] = marker

        # Check if the game has ended
        next_state = self.gamestate_cls(marker, self.board, self.board_values, move, self.kwargs)
        self.handle_next_state(next_state, ai_turn)

        # Have AI take its turn after the player
        if not self.ended and not ai_turn:
            self.ai_turn()

    def player_turn(self, move: int):
        """Create new board state from current state and player's move.
        """
        self.take_turn(move, False)

    def ai_turn(self):
        """Create new board state from current state and AI's best move.
        """
        # Update player about board state
        self.print_board()
        print('My turn! Thinking...')

        # Find best move for AI in this state
        this_state = self.gamestate_cls(GameState.PLAYER, self.board, self.board_values, -1, self.kwargs)
        ai_move = this_state.get_best_move()

        self.take_turn(ai_move, True)

    def print_board(self, print_indices=True):
        """ Print the game board.
        """
        raise NotImplementedError()
