import unitary.examples.quantum_rpg.item as item


def test_itemi_str():
    sign = item.Item(
        keyword_actions=[
            (["read", "examine"], "Keep out"),
            ("pass", "Or enter, Im a sign, not a cop"),
        ],
        description="A sign blocks the way forward.",
    )
    assert sign.get_action("read") == "Keep out"
    assert sign.get_action("examine") == "Keep out"
    assert sign.get_action("pass") == "Or enter, Im a sign, not a cop"
    assert sign.description == "A sign blocks the way forward."
