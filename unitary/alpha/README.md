Unitary - Alpha API
=============


This is a preliminary API for the Unitary game engine
to create games based on quantum computing concepts.


This API is under active design and development and is
subject to change, perhaps radically, without notice.

## Installation

From a python (virtual) environment, you can install the unitary
repository using:

```
pip install --quiet git+https://github.com/quantumlib/unitary.git
```

In colab, use:

```
!pip install --quiet git+https://github.com/quantumlib/unitary.git
```

You can then use unitary alpha API in your code by importing
unitary.alpha, such as

```
import unitary.alpha as alpha
```

## Quantum Objects

A quantum object represents one object in a quantum game that can
have a quantum state.  This will typically be a square on a board
or a single piece, though this can vary from game to game.

You can define a quantum object based on an enumeration (`Enum`) value.
An object based on an enum of two states will be represented as a Qubit
while an object based on three states will be represented as a Qutrit.
Note that support for Qutrits is still under development.

A quantum object takes a name and an enum value to initialize.
For instance,

```
import enum
class Square(enum.Enum):
  EMPTY=0
  FULL=1

example_square = alpha.QuantumObject('b1', Square.EMPTY)
```

## Quantum World

A Quantum World is a collection of quantum objects.

For instance, to represent a quantum chess board, one might do
the following:

```
board = {}
for col in 'abcdefgh':
  for rank in '3456':
     board[col+rank]= alpha.QuantumObject(col+rank, Square.EMPTY)
  for rank in '1278':
     board[col+rank]= alpha.QuantumObject(col+rank, Square.FULL)
chess_board = alpha.QuantumWorld(board.values())
```

You can then view the status of the quantum objects in a world using peek
and pop.  Note that a quantum object must be a part of a quantum world
to be operated on, and it can only be a member of one quantum world.

```
print('a1:')
print(chess_board.peek([board['a1']]))
print('a3:')
print(chess_board.peek([board['a3']]))
```

Note: pop does not quite work yet (as it requires post-selection).

## Quantum Effects

Quantum Effects can be applied to quantum objects to modify them.
Quantum objects must be added to a board before effects can be applied.

Some sample effects are `Flip` and `Split`.

For instance, we can turn on and off quantum objects by using `Flip`:

```
flip = alpha.Flip()
flip(board['a2'])
flip(board['a3'])
print('a2:')
print(chess_board.peek([board['a2']]))
print('a3:')
print(chess_board.peek([board['a3']]))
```

Now, a2 is empty and a3 is full.

We can also do a split move, such as this:

```
alpha.Split()(board['g1'], board['f3'], board['h3'])
print(chess_board.peek([board['h3']], count=100))
```

Notice that Split takes 3 quantum objects (a source and 2 targets.
Note also that peek can take a count so that more repetitions can
be done.  Using this, we see some of the measurements are EMPTY
and some are FULL.

## Quantum If

We can also do a quantum if statement that applies an effect
only if a quantum object is a certain state.  This manifests
in a "controlled" gate in the quantum world.

For instance,


```
alpha.quantum_if(board['h3']).apply(alpha.Flip())(board['h4'])
print(chess_board.peek([board['h3'], board['h4']], count=100))
```

This will show a mix of FULL and EMPTY states, but both 'h3' and
'h4' will have the same state (i.e. Bell pair).

You can also do anti-controls, such as:

```
alpha.quantum_if(board['f3']).equals(Square.EMPTY).apply(alpha.Flip())(board['f4'])
print(chess_board.peek([board['f3'], board['f4']], count=100))
```
