# Quantum RPG

This is a placeholder information page for the quantum RPG system and
reference game: "Final State Preparation".  More information will be
added here as we get closer to the official launch of the game in
August 2023.

The overall idea is that characters and adversaries will be circuits.  Each character and adversary will have actions that can modify (append) onto the circuit or measure the circuit.  The goal will be for the party to measure their character's qubits as 1's and the adversaries as 0's.


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



