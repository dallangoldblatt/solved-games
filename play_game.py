import random
import sys
import time

from games import GameState
from games.ttt import TTTGame
from games.c4 import C4Game

game_cls = {
    'ttt': TTTGame,
    'c4': C4Game
}

def coin_flip():
    print('Who goes first?')
    # Make sure the player makes a valid guess
    while True:
        guess = input('Heads (H) or Tails (T): ').lower()
        if guess in ['heads', 'head', 'h', 'tails', 'tail', 't']:
            break
        print('Invalid input.')
    guess = guess[0]
    flip = random.choice(['h' ,'t'])

    # Print a nice flip animation
    states = ['_', '  \\', '    |', '     /', '      _', '      \\', '      |', '      /']
    print('Flipping...')
    for s in states:
        time.sleep(0.15)
        print('\t   ', s)
    if flip == 'h':
        print('\t      Heads!')
    else:
        print('\t      Tails!')
    time.sleep(0.5)
    print()

    # Player goes first if guess is correct
    return guess == flip

def usage():
    print(f'Usage: python3 {sys.argv[0]} <game> [-d <board size>]')
    print('    Tic-Tac-Toe: \'ttt\'. Default options: -d 3')
    print('    Connect 4: \'c4\'. No options')

def main():
    # Check args for game argument
    game = sys.argv[1]
    if game not in game_cls:
        print(f'Unrecognized game: {game}')
        usage()
        sys.exit(0)

    try:
        # Check args for dim argument
        board_size = int(sys.argv[sys.argv.index('-d') + 1])
    except:
        if len(sys.argv) > 2:
            print(f'Unrecognized options: {" ".join(sys.argv[1:])}')
            usage()
            sys.exit(0)
        board_size = 3

    # Decide who goes first
    player_turn = coin_flip()
    if player_turn:
        print(f'You are {game_cls[game].FIRST}')
    else:
        print(f'You are {game_cls[game].SECOND}')

    # Create new Game
    game = game_cls[game](player_turn, board_size)

    # Keep playing while game has not ended
    while not game.ended:
        # Make sure the player inputs a valid move
        game.print_board()
        move_str = input('Your turn! Play a space: ').strip()
        try:
            if move_str.lower().startswith('q'):
                # Exit game
                sys.exit(0)
            move = int(move_str)
            if move < 0 or move >= len(game.board):
                # Illegal move
                raise ValueError
            elif game.board[move] == GameState.EMPTY:
                # Update game with chosen move
                game.player_turn(move)
            else:
                print('You cannot choose a non-empty space.')
        except ValueError:
            print('Invalid index.')

    # Print game results
    print('\n--------------------------\n')
    print(game.result)
    game.print_board(print_indices=False)

if __name__ == '__main__':
    if len(sys.argv) < 2 or '-h' in sys.argv or 'help' in sys.argv:
        usage()
        sys.exit(0)
    main()
