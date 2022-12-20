import io
import sys
from typing import List, Optional

from unitary.examples.quantum_rpg.qaracter import Qaracter


class Battle:
    """Class representing a battle between players and NPCs.

    This class encapsulates a list of players and enemies (NPCs),
    each of which are `QuantumWorld` objects.

    This class has functions for each side to take a turn using
    rules of the Quantum RPG, as well as a function to print out
    the status.

    Args:
        player_side: a list of player QuantumWorld objects representing
            their character sheets (initial state).
        enemy_side: a list of NPC QuantumWorld objects.
        file:  Optional IOBase file object to write output to.
            This enables the battle to write status to a file or string
            for testing.
    """

    def __init__(self,
                 player_side: List[Qaracter],
                 enemy_side: List[Qaracter],
                 file: io.IOBase = sys.stdout):
        self.player_side = player_side
        self.enemy_side = enemy_side
        self.file = file

    def print_screen(self):
        """Prints a two-column output of the battle status.

        Left side includes the players and their qubits.  Right
        side includes the NPCs and their qubits.

        Output will be written to the `file` attribute.
        """
        print('-----------------------------------------------', file=self.file)
        for i in range(max(len(self.player_side), len(self.enemy_side))):
            status = ''
            if i < len(self.player_side):
                status += f'{self.player_side[i].name} {type(self.player_side[i]).__name__}'
            else:
                status += '\t\t'
            status += '\t\t\t'
            if i < len(self.enemy_side):
                status += f'{self.enemy_side[i].name} {type(self.enemy_side[i]).__name__}'

            status += '\n'

            if i < len(self.player_side):
                status += self.player_side[i].status_line()
            else:
                status += '\t\t'
            status += '\t\t\t'
            if i < len(self.enemy_side):
                status += self.enemy_side[i].status_line()
            print(status, file=self.file)
        print('-----------------------------------------------', file=self.file)

    def take_player_turn(self, user_input: Optional[List[str]] = None):
        """Take a player's turn and record results in the battle.

        1) Retrieve the possible actions from the player.
        2) Prompt the player for which action to use.
        3) Prompt the player which NPC and qubit to target.
        4) Call the player's action to perform the action.

        Args:
            user_input: List of strings that substitute for the user's
                raw input.
        """

        # If user input is provided as an argument, then use that.
        # Otherwise, prompt from raw input.
        if user_input is not None:
            user_input = iter(user_input)
            get_user_input = lambda _: next(user_input)
        else:
            get_user_input = input

        for current_player in self.player_side:
            self.print_screen()
            print(f'{current_player.name} turn:', file=self.file)
            if not current_player.is_active():
                print(f'{current_player.name} is DOWN!', file=self.file)
                continue
            actions = current_player.actions()
            for key in actions:
                print(key, file=self.file)
            action = get_user_input('Choose your action: ')
            if action in current_player.actions():
                monster = int( get_user_input('Which enemy number: ')) + 1
                if monster < len(self.enemy_side):
                    qubit = int(get_user_input('Which enemy qubit number: ')),
                    selected_monster = self.enemy_side[monster]
                    qubit_name = selected_monster.quantum_object_name(qubit)
                    if qubit_name in selected_monster.active_qubits():
                        res = actions[action](selected_monster, qubit_name)
                        if isinstance(res, str):
                            print(res, file=self.file)
                    else:
                        print('not an active qubit', file=self.file)

    def take_npc_turn(self):
        """Take all NPC turns.

        Loop through all NPCs and call each function.
        """
        for npc in self.enemy_side:
            if not npc.is_active():
                print(f'{npc.name} is DOWN!', file=self.file)
                continue
            result = npc.npc_action(self)
            print(result, file=self.file)
