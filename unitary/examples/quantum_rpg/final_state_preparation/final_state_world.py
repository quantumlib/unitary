"""Module to combine all the zones of the RPG world into one list."""

import unitary.examples.quantum_rpg.final_state_preparation.classical_frontier as classical_frontier
import unitary.examples.quantum_rpg.final_state_preparation.oxtail_university as oxtail_university

WORLD = [*classical_frontier.CLASSICAL_FRONTIER, *oxtail_university.OXTAIL_UNIVERSITY]
