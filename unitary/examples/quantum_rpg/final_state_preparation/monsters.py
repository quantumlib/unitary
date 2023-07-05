import unitary.alpha as alpha

from unitary.examples.quantum_rpg.encounter import Encounter
from unitary.examples.quantum_rpg.npcs import BlueFoam, GreenFoam
from unitary.examples.quantum_rpg.xp_utils import EncounterXp

_BLUE_XP = EncounterXp(
    [
        [],
        [alpha.Flip(effect_fraction=0.5)],
        [alpha.Flip(effect_fraction=0.25)],
        [alpha.Flip(effect_fraction=0.125)],
        [alpha.Superposition()],
        [alpha.Phase(effect_fraction=0.375)],
    ],
    [0.35, 0.05, 0.20, 0.20, 0.10, 0.10],
)

_GREEN_XP = EncounterXp(
    [
        [],
        [alpha.Phase(effect_fraction=0.5)],
        [alpha.Phase(effect_fraction=0.25)],
        [alpha.Phase(effect_fraction=0.125)],
        [alpha.Superposition()],
        [alpha.Flip(effect_fraction=0.375)],
    ],
    [0.35, 0.05, 0.20, 0.20, 0.10, 0.10],
)


def blue_foam(number: int, prob: float = 0.5, xp=_BLUE_XP):
    return Encounter(
        [BlueFoam(f"bluey gooey {idx}") for idx in range(number)],
        probability=prob,
        description="Some blue quantum foam oozes towards you!",
        xp=xp,
    )


def green_foam(number: int, prob: float = 0.5, xp=_GREEN_XP):
    return Encounter(
        [GreenFoam(f"green goo {idx}") for idx in range(number)],
        probability=prob,
        description="Some green quantum foam oozes towards you!",
        xp=xp,
    )

