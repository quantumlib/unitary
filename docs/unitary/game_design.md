#Game Design

This guide explains principles that can help you decide how to implement quantum effects in your game idea.

## State

When you design a classical game, you define how your game objects transition from one state to another. For example, the level, heath, position, and progress of players and NPCs all change according to your game mechanics. 

A quantum game enables you to use quantum mechanics to evolve the state of your game objects. Game objects whose state changes unpredictably–in a way that feels natural, as opposed to random–are best suited to quantum effects. 

A poor choice for a quantum object might be a block that releases a coin the first time it’s knocked from below, but never again. The coin block has a finite binary state. A single interaction does a poor job of enabling the player to experience quantum effects.

An equally simple (but more interesting) choice for a quantum object might be a door. You can design your game mechanic to redirect your player to another part of your game through the door, depending on its state. Your game mechanic can enable the door to behave in unpredictable, non-random ways through a combination of quantum principles.
##Superposition
On its own, superposition is probabilistic behavior. List the states that a property of your game object can manifest. The unitary library will allow the game object to be a combination of these states, using a principle called superposition. 

When you retrieve the classical state of your object, it has a specific state (100% probability). If you create a superposition of states, the probability is shared by a combination of some or all of the states on your list (while your game object remains in a quantum state).

You can put your game object into a probabilistic state by using the `QuantumEffects` API:
   * By applying a `Split` effect.
   * By applying a `Superposition` effect.
   * By using the `effect_fraction` argument when you call an effect that supports it.

---
You can apply this principle to any property of the door, such as the destination beyond the door, whether it is locked, and so on.

---

## Entanglement

Entanglement links the fate of any two (or more) quantum objects. The relationship can be mutual (objects share a single fate) or exclusive (objects have opposite fates). In quantum mechanics, entanglement means that when you observe the classical state of one object, you immediately know something about the state of the other. 

As your quantum state grows, entangled objects can prompt non-obvious outcomes for your game objects.

You can create entanglement when you apply an effect conditionally between quantum objects, by using the `quantum_if()` method.

---
You can design a game mechanic that links properties of the door to the player’s actions in the game. For example, the location or destination of the door might be linked to other doors or rooms that the player has visited, or to a key that the player uses to unlock the door.

---

## Interference

Interference describes a situation where two or more quantum objects influence each other's outcomes. Whereas entanglement describes whether two objects are likely to be related, interference is an effect where quantum objects can make an outcome more (or less) likely.

When designed well, your player can experience interference effects unexpectedly during game play. 

Interference requires the following:
   * Your objects must be in superposition.
   * Your objects must be entangled.
   * Your objects must have phase.

You can create the opportunity for interference effects by using the `Phase` effect, or the `effect_fraction` argument when you use a `QuantumEffect` that accepts the argument.

---
The location or destination of a door might depend on previous engagements with the door. 

---

## Measurement

A quantum state is a complex superposition of classical states. When you need to control the classical flow of your game, you need to retrieve a classical state from the quantum state. This is the act of measurement.

Your game mechanic defines when you need to measure the quantum state. 

Use the `pop` method on your `QuantumWorld` object to retrieve the classical state of your quantum objects.

---
If you need to choose a destination for the player who walks through the door, you might need to measure the quantum state. 

Alternatively, you could enable your player to play in superposition if the door could send the player to multiple possible destinations. In this case, the player becomes entangled with the state of the door.

---

## Simplicity

Keep the quantum state of your game simple. A smaller quantum state makes your game easier for the player to understand. A smaller quantum state also improves your ability to run your game on a near-term quantum computer.

Simplicity is a process. Use this opportunity to think again about the division between the quantum state and the classical state of your game.

## Composability

The Unitary library allows for any quantum object to have up to four states. This attribute balances the limits of current classical computing and quantum computing hardware with expressivity and creativity.

The current set of quantum games, like Quantum Chess and Tiq Taq Toe, generate engagement through the interaction of quantum objects rather than quantum objects with a multitude of states.

When you design your quantum game, think about expanding the set of probable outcomes through the interaction of quantum objects, rather than adding more states to your object. In some cases, you might need to think differently about the data that you track about your objects. 

For ideas about working with the four-state limitation, see the following section.

## Example: Quantum Chess

In Quantum Chess, the positions of pieces on the board are the state that will be quantum.

There are multiple ways to think about position. You could assign each piece a square value. You would then have a list of 64 values, {a1, a2, … h8} assigned to each piece. Or you could assign each square a piece value, which would give you a list of 13 values assigned to each square. But an even simpler construction is to just say whether each square is “occupied” or “unoccupied”, and have a separate data structure tell you what piece is on a square if it is occupied. 

