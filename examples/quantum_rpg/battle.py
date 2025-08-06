# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import enum
from typing import List, Optional, Set

from . import game_state, input_helpers
from .qaracter import Qaracter
from .xp_utils import EncounterXp

# Size of the player side of battle status,
# for text alingment
_PLAYER_LEN = 40

_BATTLE_SEPARATOR = "-" * (_PLAYER_LEN + 20)


class BattleResult(enum.Enum):
    UNFINISHED = "Battle unfinished"
    PLAYERS_WON = "You have won the battle!"
    PLAYERS_ESCAPED = "You have escaped from the battle."
    PLAYERS_DOWN = "You have lost the battle."
    ENEMIES_ESCAPED = "Some enemies escaped the battle."


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
        self.player_side = [qar.copy() for qar in state.party]
        self.enemy_side = enemy_side
        self.file = state.file
        self.game_state = state
        self.xp = xp
        self.get_user_input = state.get_user_input

    def print_screen(self):
        """Prints a two-column output of the battle status.

        Left side includes the players and their qubits.  Right
        side includes the NPCs and their qubits.

        Output will be written to the `file` attribute.
        """
        print(_BATTLE_SEPARATOR, file=self.file)
        for i in range(max(len(self.player_side), len(self.enemy_side))):
            status = ""
            if i < len(self.player_side):
                player_status = (
                    f"{self.player_side[i].name} {self.player_side[i].class_name}"
                )
                status += f"{player_status: <{_PLAYER_LEN}}"
            else:
                status += " " * (_PLAYER_LEN)
            if i < len(self.enemy_side):
                status += f"{i+1}) {self.enemy_side[i].name} {type(self.enemy_side[i]).__name__}"

            status += "\n"

            if i < len(self.player_side):
                status += f"{self.player_side[i].status_line(): <{_PLAYER_LEN}}"
            else:
                status += " " * (_PLAYER_LEN)
            if i < len(self.enemy_side):
                status += self.enemy_side[i].status_line()
            print(status, file=self.file)
        print(_BATTLE_SEPARATOR, file=self.file)

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
                print(f"{current_player.name} is DOWN and cannot act!", file=self.file)
                continue
            actions = current_player.actions()
            descriptions = current_player.action_descriptions()
            for key in sorted(actions):
                print(f"{key}) {descriptions[key]}.", file=self.file)
            print("q) Read Quantopedia.", file=self.file)
            print("?) Help.", file=self.file)
            while True:
                action = self.get_user_input("Choose your action: ")
                if action == "?":
                    print(current_player.help(), file=self.file)
                elif action == "q":
                    seen_types: Set[str] = set()
                    for enemy in self.enemy_side:
                        enemy_type = type(enemy).__name__
                        enemy_index = enemy.quantopedia_index()
                        if enemy_type not in seen_types:
                            if self.game_state.has_quantopedia(enemy_index):
                                print(enemy.quantopedia_entry(), file=self.file)
                            else:
                                print(
                                    f"You do not have information on {enemy_type} yet.",
                                    file=self.file,
                                )
                            seen_types.add(enemy_type)
                else:
                    break
            if action in current_player.actions():
                monster, qubit = input_helpers.get_multiple_user_inputs(
                    self.get_user_input,
                    lambda: input_helpers.get_user_input_number(
                        self.get_user_input,
                        "Which enemy number: ",
                        max_number=len(self.enemy_side),
                        file=self.file,
                    ),
                    lambda: input_helpers.get_user_input_number(
                        self.get_user_input,
                        "Which enemy qubit number: ",
                        file=self.file,
                    ),
                    file=self.file,
                )
                selected_monster = self.enemy_side[monster - 1]
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

    def _print_battle_summary(self):
        """Prints a two-column output of the battle status.

        Left side includes the players and their qubits.  Right
        side includes the NPCs and their qubits.

        Output will be written to the `file` attribute.
        """
        print(_BATTLE_SEPARATOR, file=self.file)
        print("                    Battle Summary\n", file=self.file)
        print(
            f"The battle is over.  {self._determine_battle_result().value}",
            file=self.file,
        )

        for i in range(max(len(self.player_side), len(self.enemy_side))):
            status = ""
            if i < len(self.player_side):
                end_status = "Still up."
                cur_player = self.player_side[i]
                if self.cur_player.is_down():
                    end_status = "DOWN"
                elif cur_player.is_escaped():
                    end_status = "ESCAPED"
                player_status = f"{cur_player.name} {cur_player.class_name}: {end_status}"
                status += f"{player_status: <{_PLAYER_LEN}}"
            else:
                status += " " * (_PLAYER_LEN)
            if i < len(self.enemy_side):
                cur_player = self.enemy_side[i]
                end_status = "Still up."
                if cur_player.is_down():
                    end_status = "DOWN"
                elif cur_player.is_escaped():
                    end_status = "ESCAPED"
                status += f"{cur_player.name} {type(cur_player).__name__} {end_status}"
            print(status, file=self.file)

        print(_BATTLE_SEPARATOR, file=self.file)

    def loop(self) -> BattleResult:
        """Full battle loop until one side is defeated.

        Returns the result of a battle as an enum.
        """
        result = self._determine_battle_result()
        while result == BattleResult.UNFINISHED:
            result = self.take_player_turn()
            if result != BattleResult.UNFINISHED:
                self._print_battle_summary()
                return result
            result = self.take_npc_turn()
        self._print_battle_summary()
        return result
