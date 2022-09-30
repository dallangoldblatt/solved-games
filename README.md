## About

Conisder yourself a Tic-Tac-Toe or Connect 4 expert? See if you can beat this bot! 

The algorithm simulates all future board states and chooses the move that maximizes its score, assuming that you play optimally. If the simulation takes too long to reach a terminal state, a game-specific heuristic is used to score the non-terminal state's value. See [Minimax](https://en.wikipedia.org/wiki/Minimax) and [Alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) for a detailed explanation of how it works.

## Instructions

This project only uses standard Python libraries. Simply clone/download this repository and `cd` into the root directory.

Supported games:

* Tic-Tac-Toe - `ttt` - Specify NxN board size. Max-depth not yet supported for large boards
* Connect 4 - `c4` - Fixed 6x7 board size. Increasing max-depth increases difficulty

```
Usage: python3 play_game.py <game> [-m <max depth>] [-d <board size>]
    Tic-Tac-Toe: 'ttt'. Default options: -m 5 -d 3
    Connect 4: 'c4'. Default optionss: -m 5
```
