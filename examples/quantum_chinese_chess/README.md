Quantum Chinese Chess
================
This project is inspired by the [Quantum Chess project](https://quantumai.google/cirq/experiments/unitary/quantum_chess/concepts). It aims to introduce quantum moves to Chinese Chess (also called Xiangqi) so that the basic idea of quantum physics could be introduced to the players.

## How to run the game

After cloning the Unitary library you can use the following command line to run the game:
  
```
python -m examples.quantum_chinese_chess.chess
```

Currently we don't have a graphical interface. Text display is supported at Linux terminal, Mac terminal, Colab, and Sublime Terminus.

## Game rules
Game rules of Quantum Chinese Chess consist of classical and quantum rules. You may learn the classical Chinese Chess rules from the following sources:
  - [Wikipedia page](https://en.wikipedia.org/wiki/Xiangqi)
  
  - [A Chess Player’s Guide to Xiangqi | The Basics of Chinese Chess](https://www.youtube.com/watch?v=vklqOLf6mtU)
  
  - [Chess vs. Xiangqi | A Comparison of Game Pieces and Moves](https://www.youtube.com/watch?v=kptxJgEEF5A)

In addition to the classical rules, we introduce the quantum rules which allow pieces (except Kings) to split and merge:
| | Split / Merge | 
|--|--|
|Kings|N|
|Advisors|Y|
|Elephants|Y|
|Horses|Y|
|Rooks|Y|
|Cannons|Y|
|Pawns|Y|

For quantum moves, there are some restrictions that each piece needs to conform:
### Kings (a.k.a. Generals)
All moves are restricted within the `palace`. In the first version of the implementation, we don’t allow Kings to split or merge.

### Advisors (a.k.a. Guards)
All (classical, quantum) moves are restricted within the `palace`.

### Elephants (a.k.a. Bishops)
All moves are restricted within each player’s own side, i.e. not crossing the `river`. The condition "`elephant's eye is not blocked`" is checked for all elephants' moves.

### Horses (a.k.a. Knights) 
The condition "`horse's leg is not hobbled`" is checked for all horses' moves.

### Rooks (a.k.a. Chariots) 
No special restrictions.

### Cannons
For a cannon to capture a target, i.e. `fire`, there should be exactly one `cannon platform` between the cannon and the target. If there are nonzero quantum pieces and less than 2 classical pieces in between, a measurement will be performed to determine if the `fire` could be made.

### Pawns (a.k.a. Soldiers) 
No split or merge is allowed before crossing the `river`. After crossing the `river`, neither split nor merge could move backward or stay at the same location, but could only move forward or horizontally.

### Endgame rules
We still obey the `flying general rule`. As long as there is a non-zero probability of ending the game (e.g. there are no classical pieces but nonzero quantum pieces between two kings), we will measure the relevant pieces to determine whether the game ends.

## Commands
Each location on the board is represented by two chars [abcdefghi][0-9], i.e. from `a0` to `i9`. The legal commands are (`s`=source, `t`=target)
- `s1t1` to do a classical move, e.g. "a1a4"; 
- `s1^t1t2` to do a split move, e.g. "a1^b1a2";
- `s1s2^t1` to do a merge move, e.g. "b1a2^a1";

Other commands:

- `peek`: to peek (print a sample of) the current board state
- `peek all`: to print all possible board states with associated probabilities
- `undo`: to undo last move
- `help`: to see the commands list
- `exit`: to quit the game

## Quantum Concepts
### Superposition
With a split move, the board state becomes a [quantum superposition](https://en.wikipedia.org/wiki/Quantum_superposition) of two board states. For example, with "b9^a7c7", the left white horse is splitted from position b9 into a7 and c7:

<img width="292" alt="Screenshot 2024-07-21 at 11 09 31 PM" src="https://github.com/user-attachments/assets/a5f3bb23-3232-48fe-933d-327a597fa609">

And a `peek all` would show that the current board state is an equal superpostion of the following two states:

<img width="313" alt="Screenshot 2024-07-21 at 11 10 11 PM" src="https://github.com/user-attachments/assets/fb9e018d-4bec-4da4-8d68-3aa2c9048d2b">

### Entanglement
Continuing the above example, with another white move "b7e7" the left white cannon is (possibly) moved to position e7: 

<img width="293" alt="Screenshot 2024-07-21 at 11 16 36 PM" src="https://github.com/user-attachments/assets/bc946fc8-d366-4c0b-ae78-ece31fb416b4">

But instead of being a superposition of four states (i.e. white horse and cannon each occupy one of two possible locations), there are actually only two possbile states, as shown by `peek all`:

<img width="292" alt="Screenshot 2024-07-21 at 11 17 19 PM" src="https://github.com/user-attachments/assets/459a2be8-42e6-46b4-86d6-17adbcc6d5d3">

, i.e. either the horse was in `a7` and the cannon successfully moved ot `e7`, or the horse is in `c7` and the cannon did not move at all. This is an example of [quantum entanglement](https://en.wikipedia.org/wiki/Quantum_entanglement).

