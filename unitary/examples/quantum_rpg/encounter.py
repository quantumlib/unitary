import io
from typing import Optional, Sequence

import random

import unitary.examples.quantum_rpg.battle as battle
import unitary.examples.quantum_rpg.qaracter as qaracter
from typing import Sequence


class Encounter:
    """Container class for specifying encounters.

    Useful in specifying an adventure in quantum RPG.
    """

    def __init__(
        self,
        enemies: Sequence[qaracter.Qaracter] = (),
        probability: float = 1.0,
        description: Optional[str] = None,
    ):
        self.enemies = enemies
        self.probability = probability
        self.description = description

    def trigger(self) -> bool:
        """Returns True if the encounter should be triggered.

        This is based on the probability of the encounter happening.
        """
        return random.random() < self.probability

    def initiate(
        self, players: Sequence[qaracter.Qaracter], file: Optional[io.IOBase] = None
    ) -> battle.Battle:
        if file:
            return battle.Battle(players, self.enemies, file)
        return battle.Battle(players, self.enemies)
