
import random
import time
from ttt.game import Game

def main():
    # Decide who goes first
    print('Who goes first?')
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
        time.sleep(0.25)
        print('\t   ', s)
    if flip == 'h':
        print('\t      Heads!')
    else:
        print('\t      Tails!')
    print()

    # Player goes first if guess is correct
    player_turn = guess == flip
    if player_turn:
        print('You are X')
    else:
        print('You are O')

    # Create new Game
    game = Game(player_turn)

    while not game.ended:
        print()
        print('-----------------------------------')
        game.print_board()
        move = int(input('Play a space: '))
        game.player_turn(move)

    print()
    print('Game over')
    game.print_board()

if __name__ == '__main__':
    main()
