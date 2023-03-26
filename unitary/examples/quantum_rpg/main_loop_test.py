import io
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.encounter as encounter
import unitary.examples.quantum_rpg.location as location
import unitary.examples.quantum_rpg.main_loop as main_loop
import unitary.examples.quantum_rpg.npcs as npcs

EXAMPLE_WORLD = [
    location.Location(
        label="1",
        title="Lab Entrance",
        description="You stand before the entrance to the premier quantum lab.\nDouble doors lead east.",
        exits={location.Direction.EAST: "2"},
    ),
    location.Location(
        label="2",
        title="Disorganized Lab",
        description="Tables are here with tons of electronics.\nThe lab continues to the south.",
        exits={location.Direction.SOUTH: "3", location.Direction.WEST: "1"},
    ),
    location.Location(
        label="3",
        title="Cryostats",
        description="Giant aluminum cylinders hang suspended by large frames.\nRhythmic whirring of a pulse tube can be heard overhead.",
        encounters=[
            encounter.Encounter(
                [npcs.Observer("watcher")],
                description="A weird security guard approaches!",
                probability=1.0,
            )
        ],
        exits={location.Direction.NORTH: "2"},
    ),
]


def test_parse_commands() -> None:
    assert main_loop.Command.parse("x") is None
    assert main_loop.Command.parse("q") is main_loop.Command.QUIT
    assert main_loop.Command.parse("Q") is main_loop.Command.QUIT
    assert main_loop.Command.parse("Quit") is main_loop.Command.QUIT
    assert main_loop.Command.parse("quit") is main_loop.Command.QUIT


def test_simple_main_loop() -> None:
    output = io.StringIO()
    c = classes.Analyst("Mensing")
    loop = main_loop.MainLoop([c], location.World(EXAMPLE_WORLD), output)
    loop.loop(user_input=["quit"])
    assert (
        output.getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.
Exits: east.
""".strip()
    )


def test_do_simple_move() -> None:
    output = io.StringIO()
    c = classes.Analyst("Mensing")
    loop = main_loop.MainLoop([c], location.World(EXAMPLE_WORLD), output)
    loop.loop(user_input=["e", "w", "quit"])
    assert (
        output.getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.
Exits: east.

Disorganized Lab

Tables are here with tons of electronics.
The lab continues to the south.
Exits: south, west.

Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.
Exits: east.


""".strip()
    )


def test_battle() -> None:
    output = io.StringIO()
    c = classes.Analyst("Mensing")
    loop = main_loop.MainLoop([c], location.World(EXAMPLE_WORLD), output)
    loop.loop(user_input=["e", "south", "s", "1", "1", "quit"])
    assert (
        output.getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.
Exits: east.

Disorganized Lab

Tables are here with tons of electronics.
The lab continues to the south.
Exits: south, west.

Cryostats

Giant aluminum cylinders hang suspended by large frames.
Rhythmic whirring of a pulse tube can be heard overhead.
Exits: north.

A weird security guard approaches!
-----------------------------------------------
Mensing Analyst   watcher Observer
1QP (0|1> 0|0> 1?)   1QP (0|1> 0|0> 1?)
-----------------------------------------------
Mensing turn:
s
m
Sample result HealthPoint.HURT
Observer watcher measures Mensing at qubit Mensing_1
Cryostats

Giant aluminum cylinders hang suspended by large frames.
Rhythmic whirring of a pulse tube can be heard overhead.
Exits: north.
""".strip()
    )
