import re
import unitary.examples.quantum_rpg.item as item


def test_item_str():
    sign = item.Item(
        keyword_actions=[
            (["read", "examine"], ["sign", "message"], "Keep out"),
            ("pass", [], "Or enter, Im a sign, not a cop"),
        ],
        description="A sign blocks the way forward.",
    )
    assert sign.get_action("read") == "read what?"
    assert sign.get_action("examine") == "examine what?"
    assert sign.get_action("READ SIGN") == "Keep out"
    assert sign.get_action("READ MESSAGE") == "Keep out"
    assert sign.get_action("read letter") is None
    assert sign.get_action("pass") == "Or enter, Im a sign, not a cop"
    assert sign.get_action("pass sign") == "Or enter, Im a sign, not a cop"
    assert sign.get_action("pass by") == "Or enter, Im a sign, not a cop"
    assert sign.get_action("eat sign") is None
    assert sign.description == "A sign blocks the way forward."

    assert sign.get_action("") is None


def test_item_re():
    number_pad = item.Item(
        keyword_actions=[(["type"], re.compile("[0-9]+"), "valid number")],
        description="A numeric keypad.",
    )
    assert number_pad.get_action("type") == "type what?"
    assert number_pad.get_action("type abcde") is None
    assert number_pad.get_action("type 01234") == "valid number"
