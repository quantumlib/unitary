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

from typing import List, Optional, Sequence
import enum
import io
import sys

import unitary.examples.quantum_rpg.ascii_art as ascii_art
import unitary.examples.quantum_rpg.battle as battle
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.input_helpers as input_helpers
import unitary.examples.quantum_rpg.encounter as encounter
import unitary.examples.quantum_rpg.world as world
import unitary.examples.quantum_rpg.xp_utils as xp_utils
import unitary.examples.quantum_rpg.final_state_preparation.final_state_world as final_state_world


class Command(enum.Enum):
    """Command parsing utility.

    Currently only supports 'quit' but future expansion planned.
    """

    QUIT = "quit"

    @classmethod
    def parse(cls, s: str) -> Optional["Command"]:
        """Parses a string as a Direction.

        Allows prefixes, like 'e' to be parsed as EAST.
        """
        lower_s = s.lower()
        for cmd in Command:
            if cmd.value.startswith(lower_s):
                return cmd
        return None


class MainLoop:
    def __init__(self, world: world.World, state: game_state.GameState):
        self.world = world
        self.game_state = state

    @property
    def party(self):
        return self.game_state.party

    @property
    def file(self):
        return self.game_state.file

    def loop(self, user_input: Optional[Sequence[str]] = None) -> None:
        """Full battle loop until one side is defeated.

        Returns the result of a battle as an enum.
        """
        print_room_description = True
        while True:
            if print_room_description:
                print(self.world.current_location, file=self.file)
            else:
                print_room_description = True
            if self.world.current_location.encounters:
                result = None
                for random_encounter in self.world.current_location.encounters:
                    if random_encounter.will_trigger():
                        if random_encounter.description:
                            print(random_encounter.description, file=self.file)
                        current_battle = random_encounter.initiate(self.game_state)
                        result = current_battle.loop()
                        self.world.current_location.remove_encounter(random_encounter)

                        if result == battle.BattleResult.PLAYERS_WON:
                            awarded_xp = current_battle.xp
                            xp_utils.award_xp(self.game_state, awarded_xp)
                        break
                if result is not None:
                    # Reprint location description now that encounter is over.
                    print(self.world.current_location, file=self.file)

            current_input = self.game_state.get_user_input(">")
            cmd = world.Direction.parse(current_input)
            if cmd is not None:
                new_location = self.world.move(cmd)
                if new_location is not None:
                    self.game_state.current_location_label = new_location.label
                continue
            action = self.world.current_location.get_action(current_input)
            if action is not None:
                if isinstance(action, str):
                    print(action, file=self.file)
                elif callable(action):
                    msg = action(self.game_state)
                    if msg:
                        print(msg, file=self.file)
                print_room_description = False
                continue
            input_cmd = Command.parse(current_input)
            if input_cmd == Command.QUIT:
                return
            else:
                print(
                    f"I did not understand the command {current_input}", file=self.file
                )


def main(state: game_state.GameState) -> None:
    main_loop = None
    print(ascii_art.TITLE_SCREEN, file=state.file)
    while not main_loop:
        print(ascii_art.START_MENU, file=state.file)
        menu_choice = int(
            input_helpers.get_user_input_number(state.get_user_input, ">", 4)
        )
        if menu_choice == 1:
            print(ascii_art.INTRO_STORY, file=state.file)
            name = input_helpers.get_user_input_qaracter_name(
                state.get_user_input, "your initial Analyst qaracter", file=state.file
            )
            qar = classes.Analyst(name)
            state.party.append(qar)
            main_loop = MainLoop(world.World(final_state_world.WORLD), state)
        elif menu_choice == 2:
            pass
        elif menu_choice == 3:
            print(ascii_art.HELP, file=state.file)
        elif menu_choice == 4:
            return
    main_loop.loop()


if __name__ == "__main__":
    main(game_state.GameState(party=[]))
