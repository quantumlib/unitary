# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unitary.alpha as alpha

from ..encounter import Encounter
from ..npcs import BlueFoam, GreenFoam, RedFoam, PurpleFoam
from ..xp_utils import EncounterXp

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


def red_foam(number: int, prob: float = 0.5, xp=_GREEN_XP):
    return Encounter(
        [RedFoam(f"red froth {idx}") for idx in range(number)],
        probability=prob,
        description="Some energetic red quantum foam exudes towards you!",
        xp=xp,
    )


def purple_foam(number: int, prob: float = 0.5, xp=_GREEN_XP):
    return Encounter(
        [PurpleFoam(f"purple foam {idx}") for idx in range(number)],
        probability=prob,
        description="Scintillating purple quantum foam drifts towards you!",
        xp=xp,
    )
