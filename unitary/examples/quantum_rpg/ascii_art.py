"""ASCII art and other large text constants."""


# ASCII art generated with font
# DOOM by Frans P. de Vries <fpv@xymph.iaf.nl>  18 Jun 1996
# based on Big by Glenn Chappell 4/93 -- based on Standard
# figlet release 2.1 -- 12 Aug 1994
TITLE_SCREEN = r"""
______  _                _             _____  _           _
|  ___|(_)              | |           /  ___|| |         | |
| |_    _  _ __    __ _ | |    __     \ `--. | |_   __ _ | |_   ___
|  _|  | || '_ \  / _` || |    ()      `--. \| __| / _` || __| / _ \
| |    | || | | || (_| || |    )(     /\__/ /| |_ | (_| || |_ |  __/
\_|    |_||_| |_| \__,_||_|    )(     \____/  \__| \__,_| \__| \___|
                            o======o
                               ||
______                         ||              _    _
| ___ \                        ||             | |  (_)
| |_/ / _ __   ___  _ __    __ _| _ __   __ _ | |_  _   ___   _ __
|  __/ | '__| / _ \| '_ \  / _` || '__| / _` || __|| | / _ \ | '_ \
| |    | |   |  __/| |_) || (_| || |   | (_| || |_ | || (_) || | | |
\_|    |_|    \___|| .__/  \__,_||_|    \__,_| \__||_| \___/ |_| |_|
                   | |         ||
                   |_|         \/
"""


START_MENU = """
-----------------------------------------------
1) Begin new adventure
2) Load existing adventure
3) Help
4) Quit
-----------------------------------------------
""".strip()


INTRO_STORY = """
As a young analyst straight out of school,
you have heard the hype and excitement about
the quantum realm and the rumors of a great computer
that can calculate beyond what any classical device
can do.  When the call for able adventurers comes,
you are first to volunteer for the mission.  You are
given orders to report to the quantum frontier in a
quest to discover an incursion of bizarre errors that
threaten the realm.  After a long journey, you arrive
at a frontier hut where an expert awaits your arrival.
"""

HELP = """
Final state preparation is an RPG in the style of old
school text adventures.  However, instead of stats or
abilities rolled by dice, your characters (or qaracters)
are determined by a quantum circuit!

Each qaracter in your party will have a number of qubits
equal to their level, and a circuit that determines
their initial state.  If you get into a battle, you will
need to make sure that you measure your party's qubits as
1's and your opponent's qubits as 0's.  Each qaracter
also has a class that determines what actions they can do
during battle.  Some qaracters can measure qubits, and
others can apply gates.

Outside of battle, commands are similar to previous text
adventures:

  - NORTH, SOUTH, EAST, WEST, UP, DOWN can be used to move.
  - LOAD and SAVE can be used to get or apply a code to
    go back to a point in the game.
  - QUIT can be used to exit the game.

Some objects in the game can be interacted with, usually
using two-word instructions, such as 'READ SIGN' or
'EXAMINE DEVICE'.  You can also TALK to some people
who are in the room with you.
"""
