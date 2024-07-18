from ..item import EXAMINE, Item
from ..world import Direction, Location

CONSTRUCTION_SIGN = Item(
    keyword_actions=[
        (
            EXAMINE,
            "sign",
            (
                "Congratulations on making it to the end of the demo!\n"
                "The following zone (Quantum Perimeter) is still under construction.\n"
                "Come back soon for updates!"
            ),
        )
    ],
    description="A yellow and black sign denotes a warning here.",
)


QUANTUM_PERIMETER = [
    Location(
        label="perimeter1",
        title="Inside the Perimeter",
        description=(
            "You have made it inside the Quantum Perimeter Research Facility."
        ),
        encounters=[],
        items=[CONSTRUCTION_SIGN],
        exits={Direction.SOUTH: "hadamard17"},
    ),
]
