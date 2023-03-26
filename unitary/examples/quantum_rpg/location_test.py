import unitary.examples.quantum_rpg.location as location


EXAMPLE_WORLD = [
    location.Location(
        label="1", title="upper left", exits={location.Direction.EAST: "2"}
    ),
    location.Location(
        label="2",
        title="upper right",
        exits={location.Direction.SOUTH: "3", location.Direction.WEST: "1"},
    ),
    location.Location(
        label="3", title="lower right", exits={location.Direction.NORTH: "2"}
    ),
]


def test_parse_direction():
    assert location.Direction.parse("east") == location.Direction.EAST
    assert location.Direction.parse("west") == location.Direction.WEST
    assert location.Direction.parse("north") == location.Direction.NORTH
    assert location.Direction.parse("south") == location.Direction.SOUTH
    assert location.Direction.parse("up") == location.Direction.UP
    assert location.Direction.parse("down") == location.Direction.DOWN
    assert location.Direction.parse("e") == location.Direction.EAST
    assert location.Direction.parse("w") == location.Direction.WEST
    assert location.Direction.parse("n") == location.Direction.NORTH
    assert location.Direction.parse("s") == location.Direction.SOUTH
    assert location.Direction.parse("u") == location.Direction.UP
    assert location.Direction.parse("d") == location.Direction.DOWN
    assert location.Direction.parse("EAST") == location.Direction.EAST
    assert location.Direction.parse("WEST") == location.Direction.WEST
    assert location.Direction.parse("NORTH") == location.Direction.NORTH
    assert location.Direction.parse("SOUTH") == location.Direction.SOUTH
    assert location.Direction.parse("UP") == location.Direction.UP
    assert location.Direction.parse("DOWN") == location.Direction.DOWN
    assert location.Direction.parse("E") == location.Direction.EAST
    assert location.Direction.parse("W") == location.Direction.WEST
    assert location.Direction.parse("N") == location.Direction.NORTH
    assert location.Direction.parse("S") == location.Direction.SOUTH
    assert location.Direction.parse("U") == location.Direction.UP
    assert location.Direction.parse("D") == location.Direction.DOWN


def test_parse_unknown_direction():
    assert location.Direction.parse("Northwest") is None
    assert location.Direction.parse("x") is None
    assert location.Direction.parse("Z") is None


def test_location():
    world = location.World(EXAMPLE_WORLD)
    assert world.current_location.label == "1"
    assert world.move(location.Direction.NORTH) is None
    assert world.move(location.Direction.SOUTH) is None
    assert world.move(location.Direction.WEST) is None
    assert world.move(location.Direction.EAST).label == "2"
    assert world.current_location.label == "2"
    assert world.move(location.Direction.NORTH) is None
    assert world.move(location.Direction.EAST) is None
    assert world.move(location.Direction.WEST).label == "1"
    assert world.current_location.label == "1"
    assert world.move(location.Direction.EAST).label == "2"
    assert world.current_location.label == "2"
    assert world.move(location.Direction.SOUTH).label == "3"
    assert world.current_location.label == "3"
    assert world.move(location.Direction.EAST) is None
    assert world.move(location.Direction.SOUTH) is None
    assert world.move(location.Direction.WEST) is None
    assert world.move(location.Direction.NORTH).label == "2"
    assert world.current_location.label == "2"
