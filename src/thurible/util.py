"""
util
~~~~

Miscellaneous utility functions and classes for the `thurible`
package.
"""
from queue import Queue
from typing import Optional

from blessed import Terminal


# Common values.
_term: Optional[Terminal] = None


# Common classes.
class Box:
    """Create a new :class:`thurible.util.Box` object. These objects
    track the characters used to draw a frame in a terminal. It has
    fifteen properties that return the character used for that part
    of the box:

    * top: The top
    * bot: The bottom
    * side: The sides
    * mhor: Interior horizontal lines
    * mver: Interior vertical lines
    * ltop: The top-left corner
    * mtop: Top mid-join
    * rtop: The top-right corner
    * lside: Left side mid-join
    * mid: Interior join
    * rside: Right side mid-join
    * lbot: Bottom-left corner
    * mbot: Bottom mid-join
    * rbot: Bottom-right corner

    :param kind: (Optional). Sets the set of characters used by the
        :class:`thurible.util.Box` object. It defaults to light.
        Available options include double, heavy, heavy_double_dash,
        heavy_out_light_in, heavy_quadruple_dash, light,
        light_double_dash, light_quadruple_dash, light_out_heavy_in,
        light_triple_dash.
    :param custom: (Optional). Provides a custom set of characters
        for the :class:`thurible.util.Box` object to use.
    :return: None.
    :rtype: NoneType
    """
    def __init__(
        self,
        kind: str = 'light',
        custom: Optional[str] = None
    ) -> None:
        self._names = [
            'top', 'bot', 'side',
            'mhor', 'mver',
            'ltop', 'mtop', 'rtop',
            'lside', 'mid', 'rside',
            'lbot', 'mbot', 'rbot',
        ]
        self._double = '══║═║╔╦╗╠╬╣╚╩╝'
        self._heavy = '━━┃━┃┏┳┓┣╋┫┗┻┛'
        self._heavy_double_dash = '╍╍╏╍╏' + self._heavy[3:]
        self._heavy_out_light_in = '━━┃─│┏┯┓┠┼┨┗┷┛'
        self._heavy_quadruple_dash = '┉┉┋┉┋' + self._heavy[3:]
        self._heavy_triple_dash = '┅┅┇┅┇' + self._heavy[3:]
        self._light = '──│─│┌┬┐├┼┤└┴┘'
        self._light_double_dash = '╌╌╎╌╎' + self._light[3:]
        self._light_quadruple_dash = '┈┈┊┈┊' + self._light[3:]
        self._light_out_heavy_in = '──│━┃┌┰┐┝╋┥└┸┘'
        self._light_triple_dash = '┄┄┆┄┆' + self._light[3:]
        if kind:
            self.kind = kind
        else:
            self.kind = 'light'
        if custom:
            self.custom = custom
            self.kind = 'custom'

    def __getattr__(self, name):
        try:
            index = self._names.index(name)
        except ValueError:
            return self.__dict__[name]
        return self._chars[index]

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = value
        self._chars = getattr(self, f'_{value}')

    @property
    def custom(self):
        return self._custom

    @custom.setter
    def custom(self, value):
        strvalue = str(value)
        if len(strvalue) == 14:
            self._custom = str(strvalue)
            self._kind = 'custom'
        else:
            reason = 'The custom string must be 14 characters.'
            raise ValueError(reason)


# Common functions.
def get_queues() -> tuple[Queue, Queue]:
    """Create two :class:`queue.Queue` objects for use in communicating
    with a :func:`thurible.queued_manager` manager. This is just here
    for convenience, allowing you to use :func:`thurible.queued_manager`
    without having to import :mod:`queue`. It doesn't store the queues.

    :return: A :class:`tuple` objects, containing two
        :class:`queue.Queue` objects.
    :rtype: tuple
    """
    q_to: Queue = Queue()
    q_from: Queue = Queue()
    return q_to, q_from


def get_terminal() -> Terminal:
    """Retrieve an instance of :class:`blessed.Terminal` for use by
    :mod:`thurible` objects. Every time this is called, it will
    return the same instance, avoiding time wasting due to unnecessary
    :class:`Terminal` object initiation.

    .. note:
        Since we are using a mutable global value here, there may be
        theoretical thread safety concerns. However :mod:`thurible`
        doesn't ever change the :class:`Terminal` object. The only
        mutability is whether or not the :obj:`_term` is :obj:`None`
        or is a :class:`Terminal` object. So, I don't think thread
        safety will ever be a real issue for this. However, it may be
        worth looking into whether there are better ways to do this in
        the future. For all I know :class:`Terminal` may be a singleton,
        and this is entirely unnecessary.
    """
    global _term
    if not isinstance(_term, Terminal):
        _term = Terminal()
    return _term
