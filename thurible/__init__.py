"""
__init__
~~~~~~~~

Initialization for the `thurible` package.
"""
from typing import Optional

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible.menu import Menu, Option
from thurible.splash import Splash
from thurible.table import Table
from thurible.thurible import queued_manager
from thurible.text import Text


# Common values.
_term: Optional[Terminal] = None


# Common functions.
def get_terminal() -> Terminal:
    """Retrieve an instance of blessed.Terminal for use by thurible
    objects. Every time this is called, it will return the same
    instance, avoiding time wasting due to unnecessary Terminal object
    initiation.
    """
    global _term
    if not isinstance(_term, Terminal):
        _term = Terminal()
    return _term
