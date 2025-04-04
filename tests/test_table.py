"""
test_table
~~~~~~~~~~

Unit tests for the `thurible.table` module.
"""
from dataclasses import dataclass

import pytest as pt

from thurible import table as t


# Utility classes.
@dataclass
class Record:
    """A record containing test data."""
    name: str
    age: int
    parrot: bool


# Fixtures.
@pt.fixture
def records():
    return [
        Record('John', 83, True),
        Record('Michael', 79, True),
        Record('Graham', 48, False),
        Record('Terry', 77, False),
        Record('Eric', 9, False),
        Record('Terry', 81, False),
        Record('Carol', 80, False),
    ]


# Test case.
class TestTable:
    def test__init_default(
        self, content_attr_defaults_menu,
        frame_attr_defaults,
        panel_attr_defaults,
        records,
        title_attr_defaults
    ):
        panel = t.Table(
            records=records
        )
        assert panel.records == records
        assert not panel.inner_frame
        assert {
            k: getattr(panel, k) for k in content_attr_defaults_menu
        } == content_attr_defaults_menu
        assert {
            k: getattr(panel, k) for k in title_attr_defaults
        } == title_attr_defaults
        assert {
            k: getattr(panel, k) for k in frame_attr_defaults
        } == frame_attr_defaults
        assert {
            k: getattr(panel, k) for k in panel_attr_defaults
        } == panel_attr_defaults

    def test__init_set(
        self, content_attr_set,
        frame_attr_set,
        panel_attr_set,
        records,
        title_attr_set
    ):
        """Given any parameters, a TitlePanel should return an
        object with the expected attributes set.
        """
        panel = t.Table(
            records=records,
            inner_frame=True,
            **content_attr_set,
            **title_attr_set,
            **frame_attr_set,
            **panel_attr_set
        )
        assert panel.records == records
        assert panel.inner_frame
        assert {
            k: getattr(panel, k) for k in content_attr_set
        } == content_attr_set
        assert {
            k: getattr(panel, k) for k in title_attr_set
        } == title_attr_set
        assert {
            k: getattr(panel, k) for k in frame_attr_set
        } == frame_attr_set
        assert {
            k: getattr(panel, k) for k in panel_attr_set
        } == panel_attr_set

    def test_as_str(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table.
        """
        panel = t.Table(
            records=records[:5],
            height=5,
            width=20
        )
        assert str(panel) == (
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

    def test_as_str_cell_line_feed(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table. If a record contains a new_line
        character, it is replaced with a space.
        """
        records = [
            records[0],
            Record('Mic\x0aael', 79, True),
            *records[2:]
        ]
        panel = t.Table(
            records=records[:5],
            height=5,
            width=20
        )
        assert str(panel) == (
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

    def test_as_str_cell_overflow(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table. If a value is so large that the cell
        holding it cannot fit within the table, the value should be
        truncated and an overflow indicator shown.
        """
        records = [
            Record('012345678901234567890123456789', 10, False),
            *records[:4]
        ]
        panel = t.Table(
            records=records,
            height=5,
            width=20
        )
        assert str(panel) == (
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

    def test_as_str_cell_overflow_two_fields(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table. If a value is so large that the cell
        holding it cannot fit within the table, the value should be
        truncated and an overflow indicator shown. If two fields have
        values that are too large, both should overflow.
        """
        records = [
            Record(
                '012345678901234567890123456789',
                123456789012345678901234567890,
                False
            ),
            *records[:4]
        ]
        panel = t.Table(
            records=records,
            height=5,
            width=20
        )
        assert str(panel) == (
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

    def test_as_str_with_bg_and_fg(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table.
        """
        panel = t.Table(
            records=records[:5],
            height=5,
            width=20,
            bg='blue',
            fg='red'
        )
        assert str(panel) == (
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

    def test_as_str_with_overflow_bottom(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table. If the text overflows the bottom of
        the display, there should be an indicator showing there is
        overflow.
        """
        panel = t.Table(
            records=records,
            height=5,
            width=20
        )
        assert str(panel) == (
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

    def test_as_str_with_overflow_bottom_and_bg_and_fg(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table. If the text overflows the bottom of
        the display, there should be an indicator showing there is
        overflow.
        """
        panel = t.Table(
            records=records,
            height=5,
            width=20,
            bg='blue',
            fg='red'
        )
        assert str(panel) == (
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

    def test_as_str_with_content_align_h_center(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table.
        """
        panel = t.Table(
            records=records[:5],
            height=5,
            width=20,
            content_align_h='center'
        )
        assert str(panel) == (
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

    def test_as_str_with_content_align_h_right(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table. If the inner horizontal alignment is
        set to right, the cells in the rows should be aligned to the
        right.
        """
        panel = t.Table(
            records=records[:5],
            height=5,
            width=20,
            content_align_h='right'
        )
        assert str(panel) == (
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

    def test_as_str_with_inner_frame(self, records, term):
        """When converted to a string, a Table object returns a string
        that will draw the table. If inner frame is true, the fields
        should be surrounded by the inner frame.
        """
        panel = t.Table(
            records=records[:2],
            height=5,
            width=20,
            inner_frame=True,
            frame_type='light'
        )
        assert str(panel) == (
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

    def test_action_down(self, KEY_DOWN, records, term):
        """When a down arrow is received, Table.action() scrolls down
        in the text.
        """
        panel = t.Table(
            records=records,
            height=5,
            width=20
        )
        panel._overflow_bottom = True
        panel._stop = 4
        assert panel.action(KEY_DOWN) == ('', (
            f'{term.move(0, 0)}                    '
            f'{term.move(0, 8)}[▲]'
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(1, 0)}Graham  48 ▁        '
            f'{term.move(2, 0)}Terry   77 ▁        '
            f'{term.move(3, 0)}Eric     9 ▁        '
        ))

    def test_action_down_cannot_scroll_past_end(
        self, KEY_DOWN, records, term
    ):
        """When a down arrow is received, Table.action() scrolls down
        in the text. If already at the bottom of the text, Table.action()
        cannot scroll any farther.
        """
        panel = t.Table(
            records=records,
            height=5,
            width=20
        )
        panel._overflow_bottom = False
        panel._overflow_top = True
        panel._start = 3
        panel._stop = 7
        assert panel.action(KEY_DOWN) == ('', (
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(1, 0)}Terry   77 ▁        '
            f'{term.move(2, 0)}Eric     9 ▁        '
            f'{term.move(3, 0)}Terry   81 ▁        '
            f'{term.move(4, 0)}Carol   80 ▁        '
        ))

    def test_action_down_reach_near_bottom(
        self, KEY_DOWN, records, term
    ):
        """When a down arrow is received, Table.action() scrolls down
        in the text. If the bottom of the text is reached, the bottom
        overflow indicator should not be shown.
        """
        panel = t.Table(
            records=records,
            height=5,
            width=20
        )
        panel._overflow_bottom = True
        panel._overflow_top = True
        panel._start = 2
        panel._stop = 5
        assert panel.action(KEY_DOWN) == ('', (
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

    def test_action_down_arrow_with_frame_type(
        self, KEY_DOWN, records, term
    ):
        """When a down arrow is received, `Table.action()` scrolls down
        in the text. If the `Table` has a frame, the scrolled lines
        include the side frames.
        """
        panel = t.Table(
            records=records,
            height=7,
            width=20,
            frame_type='light'
        )
        panel._overflow_bottom = True
        panel._stop = 4
        assert panel.action(KEY_DOWN) == ('', (
            f'{term.move(1, 1)}                  '
            f'{term.move(1, 8)}[▲]'
            f'{term.move(2, 1)}                  '
            f'{term.move(3, 1)}                  '
            f'{term.move(4, 1)}                  '
            f'{term.move(2, 0)}│Graham  48 ▁      │'
            f'{term.move(3, 0)}│Terry   77 ▁      │'
            f'{term.move(4, 0)}│Eric     9 ▁      │'
        ))
