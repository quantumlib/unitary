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
import unitary.examples.quantum_rpg.exceptions as exceptions
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

    LOAD = "load"
    STATUS = "status"
    SAVE = "save"
    HELP = "help"
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

    def print_status(self):
        print(
            "\n".join(
                f"{idx+1}) {qar.qar_status()}"
                for idx, qar in enumerate(self.game_state.party)
            ),
            file=self.file,
        )

    def loop(self, user_input: Optional[Sequence[str]] = None) -> None:
        """Main loop of Quantum RPG.

        Loop by getting user input and then acting on it.
        """
        print_room_description = True
        try:
            while True:
                if print_room_description:
                    print(self.world.current_location, file=self.file)
                else:
                    print_room_description = True
                if self.world.current_location.encounters:
                    result = None
                    # If this location has random encounters, then see if any will
                    # trigger.  If so, initiate the battle.
                    for random_encounter in self.world.current_location.encounters:
                        if random_encounter.will_trigger():
                            if random_encounter.description:
                                print(random_encounter.description, file=self.file)
                            current_battle = random_encounter.initiate(self.game_state)
                            result = current_battle.loop()
                            self.world.current_location.remove_encounter(
                                random_encounter
                            )

                            if result == battle.BattleResult.PLAYERS_WON:
                                awarded_xp = current_battle.xp
                                xp_utils.award_xp(self.game_state, awarded_xp)
                            elif result == battle.BattleResult.PLAYERS_DOWN:
                                raise exceptions.UntimelyDeathException(
                                    "You have been defeated!"
                                )
                            elif result == battle.BattleResult.PLAYERS_ESCAPED:
                                print("You have escaped the battle!", file=self.file)
                            elif result == battle.BattleResult.ENEMIES_ESCAPED:
                                print(
                                    "The enemies have run away and escaped!",
                                    file=self.file,
                                )
                            break
                    if result is not None:
                        # Reprint location description now that encounter is over.
                        print(self.world.current_location, file=self.file)

                current_input = self.game_state.get_user_input(">")
                self.game_state.current_input = current_input
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
                        msg = action(self.game_state, self.world)
                        if msg:
                            print(msg, file=self.file)
                    print_room_description = False
                    continue
                input_cmd = Command.parse(current_input)
                if input_cmd == Command.QUIT:
                    return
                elif input_cmd == Command.STATUS:
                    self.print_status()
                elif input_cmd == Command.HELP:
                    print(ascii_art.HELP, file=self.file)
                elif input_cmd == Command.LOAD:
                    print(
                        "Paste the save file here to load the game from that point.",
                        file=self.file,
                    )
                    save_file = self.game_state.get_user_input("")
                    self.game_state.with_save_file(save_file)
                    self.world.current_location = self.world.locations[
                        self.game_state.current_location_label
                    ]
                elif input_cmd == Command.SAVE:
                    print(
                        "Use this code to return to this point in the game:",
                        file=self.file,
                    )
                    print(self.game_state.to_save_file(), file=self.file)
                    print("")
                    print_room_description = False
                else:
                    print(
                        f"I did not understand the command {current_input}",
                        file=self.file,
                    )
        except exceptions.UntimelyDeathException as e:
            print(e, file=self.file)
            print(ascii_art.RIP_TOP, file=self.file)
            for qar in self.game_state.party:
                print(f"     |       | {qar.name: ^16} |", file=self.file)
            print(ascii_art.RIP_BOTTOM, file=self.file)
            print(
                "You have been measured and were found wanting.",
                file=self.file,
            )
            print("Better luck next repetition.", file=self.file)
            return


def main(state: game_state.GameState) -> None:
    """Initial start screen for Quantum RPG.

    Display intro image and then get initial choice(s)
    to start the game.
    """
    main_loop = None
    print(ascii_art.TITLE_SCREEN, file=state.file)
    while not main_loop:
        print(ascii_art.START_MENU, file=state.file)
        menu_choice = int(
            input_helpers.get_user_input_number(
                state.get_user_input, ">", 4, file=state.file
            )
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
            print(
                "Paste the save file here to load the game from that point.",
                file=state.file,
            )
            save_file = state.get_user_input("")
            state = state.with_save_file(save_file)
            main_loop = MainLoop(world.World(final_state_world.WORLD), state)
            main_loop.world.current_location = main_loop.world.locations[
                state.current_location_label
            ]
        elif menu_choice == 3:
            print(ascii_art.HELP, file=state.file)
        elif menu_choice == 4:
            return
    main_loop.loop()


if __name__ == "__main__":
    main(game_state.GameState(party=[]))
