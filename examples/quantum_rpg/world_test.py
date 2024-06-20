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

from . import item
from . import world


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
