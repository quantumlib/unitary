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
import enum
import io
import sys
from typing import List, Optional

import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.input_helpers as input_helpers
from unitary.examples.quantum_rpg.qaracter import Qaracter
from unitary.examples.quantum_rpg.xp_utils import EncounterXp


class BattleResult(enum.Enum):
    UNFINISHED = 0
    PLAYERS_WON = 1
    PLAYERS_ESCAPED = 2
    PLAYERS_DOWN = 3
    ENEMIES_ESCAPED = 4


class Battle:
    """Class representing a battle between players and NPCs.

    This class encapsulates a list of players and enemies (NPCs),
    each of which are `QuantumWorld` objects.

    This class has functions for each side to take a turn using
    rules of the Quantum RPG, as well as a function to print out
    the status.

    Args:
        state: a GameState which contains a list of player QuantumWorld
            objects representing their character sheets (initial state).
            Includes other information, such as file objects to write ouput to.
        enemy_side: a list of NPC QuantumWorld objects.
    """

    def __init__(
        self,
        state: game_state.GameState,
        enemy_side: List[Qaracter],
        xp: Optional[EncounterXp] = None,
    ):
        self.player_side = state.party  # TODO: copy this
        self.enemy_side = enemy_side
        self.file = state.file
        self.xp = xp
        self.get_user_input = state.get_user_input

    def print_screen(self):
        """Prints a two-column output of the battle status.

        Left side includes the players and their qubits.  Right
        side includes the NPCs and their qubits.

        Output will be written to the `file` attribute.
        """
        print("-----------------------------------------------", file=self.file)
        for i in range(max(len(self.player_side), len(self.enemy_side))):
            status = ""
            if i < len(self.player_side):
                status += (
                    f"{self.player_side[i].name} {type(self.player_side[i]).__name__}"
                )
            else:
                status += "\t\t"
            status += "\t\t\t"
            if i < len(self.enemy_side):
                status += (
                    f"{self.enemy_side[i].name} {type(self.enemy_side[i]).__name__}"
                )

            status += "\n"

            if i < len(self.player_side):
                status += self.player_side[i].status_line()
            else:
                status += "\t\t"
            status += "\t\t\t"
            if i < len(self.enemy_side):
                status += self.enemy_side[i].status_line()
            print(status, file=self.file)
        print("-----------------------------------------------", file=self.file)

    def take_player_turn(self):
        """Take a player's turn and record results in the battle.

        1) Retrieve the possible actions from the player.
        2) Prompt the player for which action to use.
        3) Prompt the player which NPC and qubit to target.
        4) Call the player's action to perform the action.

        Args:
            user_input: List of strings that substitute for the user's
                raw input.
        """
        for current_player in self.player_side:
            self.print_screen()
            print(f"{current_player.name} turn:", file=self.file)
            if not current_player.is_active():
                print(f"{current_player.name} is DOWN!", file=self.file)
                continue
            actions = current_player.actions()
            for key in actions:
                print(key, file=self.file)
            action = self.get_user_input("Choose your action: ")
            if action in current_player.actions():
                monster = (
                    input_helpers.get_user_input_number(
                        self.get_user_input,
                        "Which enemy number: ",
                        max_number=len(self.enemy_side),
                        file=self.file,
                    )
                    - 1
                )
                selected_monster = self.enemy_side[monster]
                qubit = input_helpers.get_user_input_number(
                    self.get_user_input, "Which enemy qubit number: ", file=self.file
                )
                qubit_name = selected_monster.quantum_object_name(qubit)
                if qubit_name in selected_monster.active_qubits():
                    res = actions[action](selected_monster, qubit)
                    if isinstance(res, str):
                        print(res, file=self.file)
                else:
                    print(f"{qubit_name} is not an active qubit", file=self.file)
            result = self._determine_battle_result()
            if result != BattleResult.UNFINISHED:
                return result
        return BattleResult.UNFINISHED

    def take_npc_turn(self):
        """Take all NPC turns.

        Loop through all NPCs and call each function.
        """
        for npc in self.enemy_side:
            if not npc.is_active():
                print(f"{npc.name} is DOWN!", file=self.file)
                continue
            result = npc.npc_action(self)
            print(result, file=self.file)
            result = self._determine_battle_result()
            if result != BattleResult.UNFINISHED:
                return result
        return BattleResult.UNFINISHED

    def _determine_battle_result(self) -> BattleResult:
        if all(pc.is_down() for pc in self.player_side):
            return BattleResult.PLAYERS_DOWN
        if all(pc.is_down() or pc.is_escaped() for pc in self.player_side):
            return BattleResult.PLAYERS_ESCAPED
        if all(npc.is_down() for npc in self.enemy_side):
            return BattleResult.PLAYERS_WON
        if all(npc.is_down() or npc.is_escaped() for npc in self.enemy_side):
            return BattleResult.ENEMIES_ESCAPED
        return BattleResult.UNFINISHED

    def loop(self) -> BattleResult:
        """Full battle loop until one side is defeated.

        Returns the result of a battle as an enum.
        """
        result = self._determine_battle_result()
        while result == BattleResult.UNFINISHED:
            result = self.take_player_turn()
            if result != BattleResult.UNFINISHED:
                return result
            result = self.take_npc_turn()
        return result
