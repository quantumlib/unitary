# How to use the game

After cloning the Unitary library you can use command line flags to run the game:
  
```
python -m examples.tic_tac_toe.tic_tac_toe
```

## Rules of the game

There are nine positions on the 3x3 board, labeled a through h.
The object is to get three in a row.  Players alternate turns,
placing either an X or an O on each square.

In the quantum version, there is an additional move for placing
an X or an O on two squares in superposition, called the split move.

Once the board is full (i.e. each of the squares has either X,
O, or a superposition of them), the board is measured and the
result is determined.

## Quantum representation

Each square is represented as a Qutrit.  This square can either be:

*  |0> meaning that the square is empty
*  |1> meaning that the square has an X
*  |2> meaning that the square has an O

Placing an X or O will do the qutrit version of an "X" gate
on that square.  Since these are qutrits (not qubits), the
definition of this gate is that it is swapping the amplitude
of the zero state with either the one or two state
(depending on whether this is an X or O move).
For example, if someone places an O on a square, then placing
an X on that same square has no effect, since the zero state
has zero amplitude.

Note that there are two variants of the rules with regards to
the split move.  In one rule, the qutrit X gate is applied
followed by a square root of iSWAP gate (restricted to either the
|1> or |2> subspace depending on the move).

In the other variant, the corresponding states |01> and |10>
(or |02> and |20>) are swapped.

## Code organization

The qutrit operations (such as the split move) are defined in
`tic_tac_split.py`.  These classes can be used as examples of
how to create your own gates and effects using unitary.

The game itself is defined in `tic_tac_toe.py`.  The `GameInterface`
class defines the main game loop and input/output.

The `TicTacToe` class keeps track of the game state and also
allows you to sample (measure) the board.  

Enums used by the example are stored in `enums.py`.
