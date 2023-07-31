# Quantum RPG

This directory contains the rules for a Quantum RPG as well
as a reference game titled "Final State Preparation".

The overall idea is that characters and adversaries are quantum circuits.
Each character and adversary will have actions that can modify (append) to
the circuit or measure the circuit.  The goal is for the
party to measure their character's qubits as 1's and the adversaries as 0's.

This game can be used as an educational tool to learn about quantum
effects in a fun way, a base to write your own quantum RPG, or to
enjoy as a fun throwback to early text adventure games.

This README.md is divided into two parts.  The first describes
how to run and play the reference game "Final State Preparation".
The second part explains the rules and principles behind the Quantum RPG.

## Final State Preparation


### Running the game

In order to run the game, clone the github repo, make sure that any requirements
are installed with a command such as `pip install -r requirements.txt`
then run `python -m unitary.examples.quantum_rpg.main_loop`
(you may need to make sure that the Unitary library is in your PYTHONPATH).

If you do not have a python environment handy or are not familiar with setting
up python packages, you can use a colaboratory (Google/gmail account needed) that
sets it up and runs it for you.  An example can be found
[here](https://colab.sandbox.google.com/drive/1V5fQLuxrc3Zkx_z0IVDJp-SjkTj9Q2Xq).


### Adventure Start

You will start by choosing a name for the first member of your party.
This first character (or "qaracter") will be an *Analyst* that can
measure qubits.  As you continue on your journey, others may join your party.

You will start in a hut on the edge of the classical realm on a quest to
discover a solution to the problem of quantum errors that are destroying the
terrain.

To move, you can type WEST, EAST, NORTH, SOUTH, UP or DOWN to move to a new room.
You can also EXAMINE objects in the room or TALK to people who are around.

### Qaracter Sheets

Each character (and each enemy you face) will be composed of a
[quantum circuit](https://en.wikipedia.org/wiki/Quantum_circuit).
Initially, your character will start with a single qubit (Level 1)
in the initial |0〉 state.

As you progress and win battles (see below), you will gain experience
in the form of [quantum gates](https://en.wikipedia.org/wiki/Quantum_logic_gate).
These can be added to your circuit (character sheet).  Once each qubit has as
many gates on it as your level (number of qubits), you will gain a level and
a new qubit.  For example, a level 3 qaracter needs 4 gates on each of their
three qubits to advance to level 4.


### Battle

While exploring the world of **Final State Preparation**, you will eventually
chance on a battle with enemies, and text such as the below will be displayed:


```
------------------------------------------------------------
Doug Analyst                            1) bluey gooey 0 BlueFoam
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
                                        2) bluey gooey 1 BlueFoam
                                        1QP (0|1> 0|0> 1?)
                                        3) bluey gooey 2 BlueFoam
                                        1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Doug turn:
m) Measure enemy qubit.
h) Help.
```

Your party will displayed on the left.  In this case, it is a single character
named Doug of the Analyst class.

The enemies will be displayed on the right.   Here, Doug is facing
three BlueFoam enemies.

Each of these will have a status line that says how many qubits
they have and in what state they are in.

For instance, `1QP (0|1> 0|0> 1?)` means that the character has 1 qubit (1QP).
None of the qubits have been measured in the 1 state (`0|1>`) or the 0 state
(`0|1>`). 1 qubit is still unmeasured (`1?`).

Once a character (or enemy) has measured half or more qubits in the |0> state,
they are **DOWN**.  If half or more are measured in the |1> state, they
**ESCAPED**.  If all enemies are **DOWN**, you win the battle!  If some
enemies have **ESCAPED**, then the battle is over, but you do not get XP.
If all party members are **DOWN**, you lose the game.

Each round, each party member can perform an action based on their class
(such as measure a qubit).  Then, each enemy will get an action.

### Quantum Foam

The first enemies you will meet are quantum foam, representative of the
quantum errors that have prompted your journey.  Different quantum foam
begin in different states when battle begins.  A blue foam will start
in the |0〉 state, a red foam will start in a |1〉 state, and a purple
foam will start in a superposition of the two states.

Some monsters may have more complicated circuits.  You will need to search
in the world (try to find libraries) in order to find more information on them.




## Definitions

### Quantum Master (QM):

The quantum master is defined as the entity running the game.  For a table top version of the game, this can be a human organizer that chooses battles and events for the players.  For a video game version, this can be a game engine that chooses battles based on a predefined story arc or random generation.

### Character:

A character (or qaracter) is defined by a set of qubits, a set of possible actions/abilities, and a state preparation circuit (known as the qaracter's background).  A qaracter begins the initial game as a width one circuit with no quantum gates.

### Character advancement:

As a qaracter, continues on their quantum quest, they will evolve and grow.  Different momentous events in their journey can cause them to gain qaracter depth as they experience more of the quantum world.  After momentous battles or character events, the QM will decide on an appropriate award for the battle in the form of a quantum gate.
Once the state preparation circuit has depth of (the current width plus one), the character gains one width and adds a new qubit to their qaracter.
As characters advance in width, new actions are unlocked for use in resolving battles.

## Battle Semantics:

Setup:

Each battle will consist of a set of characters, a set of adversaries, and an optional environment.  Each character and adversary will have a set of qubits on which their state preparation circuit will have already been added.  The environment has no qubits.

Turn order:

* Each adversary will perform its actions.
* Each character will perform its actions.
* The environment will perform its actions, if any.
* Typically, the environment's action will be measurement-related.


#### Battle completion:

The battle is complete once all qubits for a given side have been measured.
The party has won if the following conditions are met:
Each adversary has a number of qubits measured in the zero state greater than half of their width.
At least one party member has half their qubits in either an unmeasured state or in the one state.
Alternatively,
If all party members have half or more of their qubits in the zero state, all party members are "down" and the party has been defeated.
If at least one party member is not down, but (at least) one adversary has half or more qubits in an unmeasured or one state, the adversary has survived or escaped.  If all adversaries escape, the party is not victorious.  In a battle with multiple adversaries, if some adversaries are defeated but others escape, the party is partially victorious.

#### Resolution:

If, at any time, a character has half or more of its qubits measured as 0, the character is "down".  They cannot perform any actions or participate in any battles until revived.

#### Exhaustion

If at any time, the circuit for a character becomes too large to simulate, the character is "exhausted".  If the exhaustion is due to the depth of the circuit and/or entanglement with ancilla, the character can be revived by applying cirq.Reset gates (ie. reset potions) to each affected qubit.  If the character can no longer be simulated due to the width and depth of the state preparation circuit, the character has become "overpowered" and should now be retired.


## Qaracter Classes

### Analyst

The analyst is the class for starting the game.

**Actions:**

* Level 1:  m. Analyst can measure an adversary's qubit.
* Level 1:  s. Analyst can sample (without measuring) one qubit.


### Engineeer


Actions:
* Level 1: Engineer can perform an X gate on an adversary's qubit.
* Level 3: Engineer can perform an H gate on an adversary's qubit.



