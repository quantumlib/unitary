# Fox in a Hole (Classical and Quantum version)

This game is based on the well known puzzle Fox in a Hole: There are 5 holes in a row, one of which occupied by the fox. Each day you can inspect one of the holes. Each night the fox moves to a neighboring hole. Find a strategy with which you can guaranteedly find the fox in finite days (e.g. in 10 days).

You can play the game in the classical way, as wall as in the quantum way. 

## Rules of the classical version of the game
The fox starts in a random hole. The following repeats until the player finds the fox, exceeds 10 guesses or stops the game:
1.  The player can guess which hole the fox hides in. If the player guessed well, the player wins.
2.  The fox randomly moves one hole left or right. (In the sides only one direction is possible.)

At the end of the game the program will print out for each day what the fox did and which hole the fox hid in.

## Rules of the quantum version of the game
The fox starts in a random hole. The following repeats until the player finds the fox, exceeds 10 guesses or stops the game:
1.  The player can guess which hole the fox hides in. This implies a measurement on that hole. If the fox is found to be in the guessed hole the player wins.
2.  The fox randomly choose from the following move-options:
    * Moving left (provided the starting hole is not the left-most one and the fox is in that hole with non-zero probability)
    * Moving right (provided the starting hole is not the right-most one and the fox is in that hole with non-zero probability)
    * Moving left and right at the same time (provided the starting hole is not the left-most or right-most one and the fox is in that hole with non-zero probability)

At the end of the game the program will print out for each day what the guess was, what the fox did, and which hole the fox hid in.

# How to use the game

This is a command line game. You can use command line flags to set up the game type.

    python3 fox-in-a-hole.py [-q] [-i]

| Flag | Description |
|------|-------------|
| -q | Play the quantum version of the game. Without this the classical version will run. |
| -i | For quantum moves/splits use iSWAP, instead of SWAP. |
   
