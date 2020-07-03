
import random
import time

def main():
    # Decide who goes first
    print('Who goes first?')
    while True:
        guess = input('Heads (H) or Tails (T)?: ').lower()
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

    # Max goes first if guess is correct
    max_turn = guess == flip

    print(guess, flip)


if __name__ == '__main__':
    main()
