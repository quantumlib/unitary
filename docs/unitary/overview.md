#Overview

Unitary is a library that enables game developers to add quantum behavior to their games. 

The Unitary library is designed for people who have no knowledge of quantum mechanics. The library relies on common computational metaphors like stacks, objects, and so on.

If this library is successful, anyone with intermediate knowledge of programming should be able to add quantum behavior to their program by making small changes to how they think about their data and algorithms. 


##What kinds of games?

Unitary is written in Python, so the library is best suited to casual games where game actions are not time sensitive. Board games, turn-based games, and simple 2D games would be suitable.

##What are quantum games?

Quantum games express their core mechanics by using the same maths used in quantum information science. As a result, players experience quantum effects like superposition, entanglement, and interference with no extraordinary effort from the game developer.

Through their actions in the game, players create a quantum state and trigger measurements of that state. 

Quantum Chess was the first, truly quantum, commercial game. In fact, Google’s quantum computer was used to run a game of Quantum Chess in 2020. An open-source version of Quantum Chess is included in the Unitary library.

##Why another quantum software library?

Unitary helps game designers and developers create new game mechanics by managing game state transitions and calculations. 

Before Unitary, games were based on classical mechanics, such as simple probability and standard physics. However, knowledge of quantum mechanics is rare and perceived as inaccessible to most people. Before Unitary, quantum information science was inaccessible to game developers as a design tool.

Other quantum software libraries are aimed at researchers who are developing quantum algorithms and software.

Unitary aims to make quantum information science accessible (as a design tool) for a much larger group of people.


#Core Concepts

Unitary offers an API built around the following concepts.

**Quantum Objects** store data about (classical) the state of a game object. You can use a `QuantumObject` in the same way that you would use a standard Python object to track data about things in your game. However, the state of the `QuantumObject` is influenced by Quantum Effects.

**Quantum Effects** update the state of a quantum object according to the rules of quantum mechanics. In a classical game, you update the fields of your Python object to reflect the evolving state of the game. For example, you might move a game piece by updating its X and Y coordinates, or by updating a data structure that tracks occupancy in a board object. 

A `QuantumEffect` modifies the state of one or more quantum objects by using the maths that describe quantum behavior. For example, you might move a game piece from one square into a superposition of two squares by applying a `Split` effect. Your game rules determine when you apply a `QuantumEffect` to quantum objects.

A **Quantum World** defines the scope for your quantum effects. In a classical game, the onus is on you to write code to define how game objects relate to each other, according to the model of your game world. In a quantum game, any set of quantum objects could become entangled with each other, depending on the quantum effects that you applied to your quantum objects. When calculating the outcome of quantum effects, the quantum engine needs access to the complete set of quantum objects, in principle. The `QuantumWorld` object acts as a container for the collection of all quantum objects and quantum effects on behalf of the quantum engine.

A single quantum world represents a multiverse of possibilities; we call that multiverse the quantum state. Regular game play should add quantum effects to the quantum world, where the effects apply to one or more quantum objects in the world. As game play progresses, you should build up the quantum state: quantum effects can split and entangle your quantum objects.

## Measurement

One of your tasks as the game designer is to decide when you need to “score” the game. A scoring event could be based on any intermediate classical state that makes sense for your game mechanic. For example, a game might generate a score at the end of a battle, the end of a round, or the end of the game.

When you need to score the game, you should use the `pop` method to retrieve the classical state from your `QuantumWorld` object. You can use the classical state to calculate the appropriate score for your game. 

## Quantum state and classical state

The root difference between quantum and classical state is certainty.

The quantum state that you build in a `QuantumWorld` is not deterministic. You cannot be certain which state your quantum objects are in until you “observe” them. Consequently, you can think of the classical state that you retrieve from the `pop` method as the observation (measurement) of your quantum state. 

Again, each `QuantumObject` only has a definite, classical state after you retrieve it from the `pop` method. 

At any time before you `pop` the classical state from a `QuantumWorld` object, you can retrieve a sample classical state by using the `peek` method. The `QuantumWorld` can return as many samples from your quantum state as you find useful. You can also retrieve a summary of the probability distribution of the state of your Quantum Object by calling the `get_histogram` method. You should use the `pop` method to score your game state, and you can use the `peek` method to provide information to your players.

In the real world, if you observe a single quantum state configuration twice, you might see two different classical states. To support consistent evolution of game play, the `QuantumWorld` snapshots the classical state after you call `pop`. You can continue to add quantum effects to your `QuantumWorld`, but your new quantum effects will use the classical state snapshot as the starting state for all of your quantum objects. 

## Sampler

The **Sampler** calculates the classical state of your `QuantumWorld`. Unitary is designed to use real quantum computers and quantum simulators. The `QuantumWorld` object can use any quantum computer that runs quantum circuits programmed with the Cirq library from Google Quantum AI. Samplers can be simulators (using a classical computer to calculate estimated probabilities) or can use actual quantum hardware, if you have access to a quantum processor through cirq.

Unitary includes a high performance simulator, which is optimal for use in your game. However, you can use any simulator that is compatible with Cirq.
