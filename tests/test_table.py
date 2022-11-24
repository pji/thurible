"""
test_table
~~~~~~~~~~

Unit tests for the `thurible.table` module.
"""
from dataclasses import dataclass
import unittest as ut

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible import table as t
import tests.test_panel as tp


# Utility classes.
@dataclass
class Record:
    """A record containing test data."""
    name: str
    age: int
    parrot: bool


# Common values.
term = tp.term
KEY_DOWN = Keystroke('\x1b[B', term.KEY_DOWN, 'KEY_DOWN')
KEY_END = Keystroke('\x1b[F', term.KEY_END, 'KEY_END')
KEY_HOME = Keystroke('\x1b[H', term.KEY_HOME, 'KEY_HOME')
KEY_PGDOWN = Keystroke('\x1b[U', term.KEY_PGDOWN, 'KEY_PGDOWN')
KEY_PGUP = Keystroke('\x1b[V', term.KEY_PGUP, 'KEY_PGUP')
KEY_UP = Keystroke('\x1b[A', term.KEY_UP, 'KEY_UP')
X = Keystroke('x', 0x78, 'x')


# Test case.
class TableTestCase(tp.TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a Table should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Terry', 81, False),
                Record('Eric', 79, False),
            ],
            'inner_frame': True,
            **tp.kwargs_content_opt_default_alt,
            **tp.kwargs_title_opt_set,
            **tp.kwargs_frame_opt_set,
            **tp.kwargs_panel_req,
            **tp.kwargs_panel_opt_set,
        }

        # Run test.
        table = t.Table(**exp)

        # Gather actuals.
        act = {key: getattr(table, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a Table should
        return an object with the expected attributes set.
        """
        # Expected values.
        exp_req = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Terry', 81, False),
                Record('Eric', 79, False),
            ],
            **tp.kwargs_panel_req,
        }
        exp_opt = {
            'inner_frame': False,
            **tp.kwargs_content_opt_default_alt,
            **tp.kwargs_title_opt_default,
            **tp.kwargs_frame_opt_default,
            **tp.kwargs_panel_opt_default
        }

        # Run test.
        table = t.Table(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(table, key) for key in exp_req}
        act_opt = {key: getattr(table, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a Table object returns a string
        that will draw the table.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(0, 0)}John    83 █        '
            f'{term.move(1, 0)}Michael 79 █        '
            f'{term.move(2, 0)}Graham  48 ▁        '
            f'{term.move(3, 0)}Terry   77 ▁        '
            f'{term.move(4, 0)}Eric     9 ▁        '
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__cell_line_feed(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If a record contains a new_line
        character, it is replaced with a space.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(0, 0)}John    83 █        '
            f'{term.move(1, 0)}Mic ael 79 █        '
            f'{term.move(2, 0)}Graham  48 ▁        '
            f'{term.move(3, 0)}Terry   77 ▁        '
            f'{term.move(4, 0)}Eric     9 ▁        '
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Mic\x0aael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__cell_overflow(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If a value is so large that the cell
        holding it cannot fit within the table, the value should be
        truncated and an overflow indicator shown.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(0, 0)}012345678901[▸] 10 ▁'
            f'{term.move(1, 0)}John            83 █'
            f'{term.move(2, 0)}Michael         79 █'
            f'{term.move(3, 0)}Graham          48 ▁'
            f'{term.move(4, 0)}Terry           77 ▁'
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('012345678901234567890123456789', 10, False),
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__cell_overflow_two_fields(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If a value is so large that the cell
        holding it cannot fit within the table, the value should be
        truncated and an overflow indicator shown. If two fields have
        values that are too large, both should overflow.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(0, 0)}012345[▸] 12345[▸] ▁'
            f'{term.move(1, 0)}John            83 █'
            f'{term.move(2, 0)}Michael         79 █'
            f'{term.move(3, 0)}Graham          48 ▁'
            f'{term.move(4, 0)}Terry           77 ▁'
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record(
                    '012345678901234567890123456789',
                    123456789012345678901234567890,
                    False),
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bg_and_fg(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If foreground and background colors
        are set, the contents should be those colors.
        """
        # Expected values.
        exp = (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.normal}'
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}John    83 █        '
            f'{term.move(1, 0)}Michael 79 █        '
            f'{term.move(2, 0)}Graham  48 ▁        '
            f'{term.move(3, 0)}Terry   77 ▁        '
            f'{term.move(4, 0)}Eric     9 ▁        '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
            'bg': 'blue',
            'fg': 'red',
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_overflow_bottom(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If the text overflows the bottom of
        the display, there should be an indicator showing there is
        overflow.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(4, 8)}[▼]'
            f'{term.move(0, 0)}John    83 █        '
            f'{term.move(1, 0)}Michael 79 █        '
            f'{term.move(2, 0)}Graham  48 ▁        '
            f'{term.move(3, 0)}Terry   77 ▁        '
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
                Record('Terry', 81, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_overflow_bottom_and_bg_and_fg(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If the text overflows the bottom of
        the display, there should be an indicator showing there is
        overflow. If foreground and background colors are set, the
        contents should be those colors.
        """
        # Expected values.
        exp = (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.normal}'
            f'{term.red_on_blue}'
            f'{term.move(4, 0)}                    '
            f'{term.move(4, 8)}[▼]'
            f'{term.normal}'
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}John    83 █        '
            f'{term.move(1, 0)}Michael 79 █        '
            f'{term.move(2, 0)}Graham  48 ▁        '
            f'{term.move(3, 0)}Terry   77 ▁        '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
                Record('Terry', 81, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
            'bg': 'blue',
            'fg': 'red',
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_align_h_center(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If the inner horizontal alignment is
        set to center, the cells in the rows should be aligned to the
        center.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(0, 0)}    John    83 █    '
            f'{term.move(1, 0)}    Michael 79 █    '
            f'{term.move(2, 0)}    Graham  48 ▁    '
            f'{term.move(3, 0)}    Terry   77 ▁    '
            f'{term.move(4, 0)}    Eric     9 ▁    '
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
            ],
            'content_align_h': 'center',
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_inner_align_h_right(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If the inner horizontal alignment is
        set to right, the cells in the rows should be aligned to the
        right.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(0, 0)}        John    83 █'
            f'{term.move(1, 0)}        Michael 79 █'
            f'{term.move(2, 0)}        Graham  48 ▁'
            f'{term.move(3, 0)}        Terry   77 ▁'
            f'{term.move(4, 0)}        Eric     9 ▁'
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
            ],
            'content_align_h': 'right',
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_inner_frame(self):
        """When converted to a string, a Table object returns a string
        that will draw the table. If inner frame is true, the fields
        should be surrounded by the inner frame.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 1)}                  '
            f'{term.move(2, 1)}                  '
            f'{term.move(3, 1)}                  '
            f'{term.move(0, 0)}┌──────────────────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 19)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 19)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 19)}│'
            f'{term.move(4, 0)}└──────────────────┘'
            f'{term.move(0, 8)}┬'
            f'{term.move(4, 8)}┴'
            f'{term.move(0, 11)}┬'
            f'{term.move(4, 11)}┴'
            f'{term.move(1, 0)}│John   │83│█      │'
            f'{term.move(2, 0)}├───────┼──┼───────┤'
            f'{term.move(3, 0)}│Michael│79│█      │'
        )

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
            ],
            'inner_frame': True,
            'height': 5,
            'width': 20,
            'term': term,
            'frame_type': 'light',
        }
        table = t.Table(**kwargs)

        # Run test.
        act = str(table)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow(self):
        """When a down arrow is received, Table.action() scrolls down
        in the text.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}                    '
            f'{term.move(0, 8)}[▲]'
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(1, 0)}Graham  48 ▁        '
            f'{term.move(2, 0)}Terry   77 ▁        '
            f'{term.move(3, 0)}Eric     9 ▁        '
        ))

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
                Record('Terry', 81, False),
                Record('Carol', 80, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)
        table._overflow_bottom = True
        table._stop = 4
        key = KEY_DOWN

        # Run test.
        act = table.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_cannot_scroll_past_end(self):
        """When a down arrow is received, Table.action() scrolls down
        in the text. If already at the bottom of the text, Table.action()
        cannot scroll any farther.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(1, 0)}Terry   77 ▁        '
            f'{term.move(2, 0)}Eric     9 ▁        '
            f'{term.move(3, 0)}Terry   81 ▁        '
            f'{term.move(4, 0)}Carol   80 ▁        '
        ))

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
                Record('Terry', 81, False),
                Record('Carol', 80, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)
        table._overflow_bottom = False
        table._overflow_top = True
        table._start = 3
        table._stop = 7
        key = KEY_DOWN

        # Run test.
        act = table.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_reach_near_bottom(self):
        """When a down arrow is received, Table.action() scrolls down
        in the text. If the bottom of the text is reached, the bottom
        overflow indicator should not be shown.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(1, 0)}Terry   77 ▁        '
            f'{term.move(2, 0)}Eric     9 ▁        '
            f'{term.move(3, 0)}Terry   81 ▁        '
            f'{term.move(4, 0)}Carol   80 ▁        '
        ))

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
                Record('Terry', 81, False),
                Record('Carol', 80, False),
            ],
            'height': 5,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)
        table._overflow_bottom = True
        table._overflow_top = True
        table._start = 2
        table._stop = 5
        key = KEY_DOWN

        # Run test.
        act = table.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_with_frame_type(self):
        """When a down arrow is received, `Table.action()` scrolls down
        in the text. If the `Table` has a frame, the scrolled lines
        include the side frames.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(1, 1)}                  '
            f'{term.move(1, 8)}[▲]'
            f'{term.move(2, 1)}                  '
            f'{term.move(3, 1)}                  '
            f'{term.move(4, 1)}                  '
            f'{term.move(2, 0)}│Graham  48 ▁      │'
            f'{term.move(3, 0)}│Terry   77 ▁      │'
            f'{term.move(4, 0)}│Eric     9 ▁      │'
        ))

        # Test data and state.
        kwargs = {
            'records': [
                Record('John', 83, True),
                Record('Michael', 79, True),
                Record('Graham', 48, False),
                Record('Terry', 77, False),
                Record('Eric', 9, False),
                Record('Terry', 81, False),
                Record('Carol', 80, False),
            ],
            'frame_type': 'light',
            'height': 7,
            'width': 20,
            'term': term,
        }
        table = t.Table(**kwargs)
        table._overflow_bottom = True
        table._stop = 4
        key = KEY_DOWN

        # Run test.
        act = table.action(key)

        # Determine test result.
        self.assertEqual(exp, act)
