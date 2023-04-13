import unitary.examples.quantum_rpg.world as world


EXAMPLE_WORLD = [
    world.Location(label="1", title="upper left", exits={world.Direction.EAST: "2"}),
    world.Location(
        label="2",
        title="upper right",
        exits={world.Direction.SOUTH: "3", world.Direction.WEST: "1"},
    ),
    world.Location(label="3", title="lower right", exits={world.Direction.NORTH: "2"}),
]


def test_parse_direction():
    assert world.Direction.parse("east") == world.Direction.EAST
    assert world.Direction.parse("west") == world.Direction.WEST
    assert world.Direction.parse("north") == world.Direction.NORTH
    assert world.Direction.parse("south") == world.Direction.SOUTH
    assert world.Direction.parse("up") == world.Direction.UP
    assert world.Direction.parse("down") == world.Direction.DOWN
    assert world.Direction.parse("e") == world.Direction.EAST
    assert world.Direction.parse("w") == world.Direction.WEST
    assert world.Direction.parse("n") == world.Direction.NORTH
    assert world.Direction.parse("s") == world.Direction.SOUTH
    assert world.Direction.parse("u") == world.Direction.UP
    assert world.Direction.parse("d") == world.Direction.DOWN
    assert world.Direction.parse("EAST") == world.Direction.EAST
    assert world.Direction.parse("WEST") == world.Direction.WEST
    assert world.Direction.parse("NORTH") == world.Direction.NORTH
    assert world.Direction.parse("SOUTH") == world.Direction.SOUTH
    assert world.Direction.parse("UP") == world.Direction.UP
    assert world.Direction.parse("DOWN") == world.Direction.DOWN
    assert world.Direction.parse("E") == world.Direction.EAST
    assert world.Direction.parse("W") == world.Direction.WEST
    assert world.Direction.parse("N") == world.Direction.NORTH
    assert world.Direction.parse("S") == world.Direction.SOUTH
    assert world.Direction.parse("U") == world.Direction.UP
    assert world.Direction.parse("D") == world.Direction.DOWN


def test_parse_unknown_direction():
    assert world.Direction.parse("Northwest") is None
    assert world.Direction.parse("x") is None
    assert world.Direction.parse("Z") is None
    assert world.Direction.parse("") is None


def test_location():
    example_world = world.World(EXAMPLE_WORLD)
    assert example_world.current_location.label == "1"
    assert example_world.move(world.Direction.NORTH) is None
    assert example_world.move(world.Direction.SOUTH) is None
    assert example_world.move(world.Direction.WEST) is None
    assert example_world.move(world.Direction.EAST).label == "2"
    assert example_world.current_location.label == "2"
    assert example_world.move(world.Direction.NORTH) is None
    assert example_world.move(world.Direction.EAST) is None
    assert example_world.move(world.Direction.WEST).label == "1"
    assert example_world.current_location.label == "1"
    assert example_world.move(world.Direction.EAST).label == "2"
    assert example_world.current_location.label == "2"
    assert example_world.move(world.Direction.SOUTH).label == "3"
    assert example_world.current_location.label == "3"
    assert example_world.move(world.Direction.EAST) is None
    assert example_world.move(world.Direction.SOUTH) is None
    assert example_world.move(world.Direction.WEST) is None
    assert example_world.move(world.Direction.NORTH).label == "2"
    assert example_world.current_location.label == "2"
