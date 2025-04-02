"""
test_init
~~~~~~~~~

Unit tests for the initiation of the `thurible` module.
"""
import thurible.__init__ as init


# Test case.
def test_get_terminal_stores_terminal():
    """When called multiple times, `get_terminal()` will return the
    same instance of `blessed.Terminal` rather than creating a new
    instance.
    """
    assert init.get_terminal() == init.get_terminal()
