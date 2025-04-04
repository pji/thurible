"""
test_util
~~~~~~~~~

Unit tests for the `thurible.util` module.
"""
import pytest as pt

from thurible import util


class TestBox:
    def test_normal(self):
        "A Box object should return box characters."""
        box = util.Box()
        assert box.top == '\u2500'
        assert box.bot == '\u2500'
        assert box.side == '\u2502'
        assert box.ltop == '\u250c'
        assert box.rtop == '\u2510'
        assert box.mtop == '\u252c'
        assert box.lbot == '\u2514'
        assert box.rbot == '\u2518'
        assert box.mbot == '\u2534'
        assert box.lside == '\u251c'
        assert box.rside == '\u2524'
        assert box.mid == '\u253c'

    def test_change_type(self):
        """If given a kind, the kind property should change the kind
        attribute and the _chars attribute.
        """
        box = util.Box('light')
        assert box.top == '\u2500'

        box.kind = 'heavy'
        assert box.top == '\u2501'

        box.kind = 'light_quadruple_dash'
        assert box.top == '\u2508'

    def test_custom(self):
        """If given a kind of 'custom' string of characters, the box
         object should return the custom characters and it's kind
         should be 'custom'.
        """
        box = util.Box(custom='abcdefghijklmn')
        assert box.kind == 'custom'
        assert box._chars == 'abcdefghijklmn'
        assert box.mtop == 'g'

    def test_invalid_custom_string(self):
        """The passed custom string is not exactly fourteen characters
        long, a ValueError should be raised.
        """
        with pt.raises(ValueError):
            _ = util.Box(custom='bad')
