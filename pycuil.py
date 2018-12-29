# PyCUIL -- Python Console User Interface Library


import curses

import attr


@attr.s
class UI(object):
    mainloop = attr.ib()
    _scr = attr.ib(init=None, default=None)
    _key = attr.ib(init=None, default="")
    _next_id = attr.ib(init=None, default=0)
    _hot_item = attr.ib(init=None, default=None)
    _last_id = attr.ib(init=None, default=0)
    refresh_needed = attr.ib(init=None, default=False)


    def start(self, stdscr):
        """
        Initialize the underlying console drawing API (be it ncurses or
        whatever else is supported), then kick off the application's mainloop.
        """
        self._scr = stdscr
        self.clear()
        self.mainloop(self)

    def wait_event(self):
        """
        Waits for an event at the keyboard.  The received keycode will be cached
        for later use by the application's mainloop.
        """
        self._key = self._scr.getkey()
        print(hex(ord(self._key)))


    def next_id(self):
        """
        Returns the next available ID for the purposes of uniquely identifying
        controls.
        """
        j = self._next_id
        self._next_id = self._next_id + 1
        return j

    def needs_refresh(self):
        self.refresh_needed = True

    def button(self, x, y, label, hotkey):
        """
        Render a button on the screen.

        Returns True if the button is activated, either by the hotkey provided
        or through some other reasonable means.  If no hotkey is desired,
        provide None.  Otherwise, any curses-compatible string representation
        can be used (e.g., `^G` for CTRL-G, `KEY_F(1)` for F1, etc.).
        """
        was_hit = False

        s = self._scr
        j = self.next_id()

        # Check to see if there is a hot item.  If not, assume we're it.
        # This facilitates tab navigation.
        if not self._hot_item:
            self._hot_item = j

        # The button was activated via hotkey
        if hotkey and (hotkey == self._key):
            self._hot_item = j
            self._key = ""
            was_hit = True

        # The button was activated via the RETURN key
        if (hotkey == '\x0A') and (self._hot_item == j):
            self._key = ""
            was_hit = True

        # Implement TAB/shift-TAB (or TAB/CTRL-P) navigation.
        if (self._hot_item == j) and (self._key == "\t"):
            self._hot_item = 0
            self._key = ""

        if (self._hot_item == j) and (self._key == '\x10'):
            self._hot_item = self._last_id
            self._key = ""

        self._last_id = j

        # Draw the button -- this must be the last thing we do
        # or else you'll get weird visual artifacts when handling
        # TAB navigation.
        if self._hot_item == j:
            s.addstr(y, x, "[{}]".format(label))
        else:
            s.addstr(y, x, " {} ".format(label))

        return was_hit

    def clear(self):
        """
        Clears the whole screen.
        """
        self._scr.clear()
        self._next_id = 1
        self.refresh_needed = False

    def label(self, x, y, string):
        """
        Render a plain string.  Labels cannot be activated.
        """
        self._scr.addstr(y, x, string)

    def frame(self, left, top, right, bottom):
        """
        Draws a frame with an optional label (which can be None).  A frame is
        just a convenient box around a grouping of related gadgets.  It cannot
        be activated.
        """
        s = self._scr

        left = max(left, 0)
        top = max(top, 0)
        right = min(right, curses.COLS)
        bottom = min(bottom, curses.LINES)

        if left > right:
            return

        if top > bottom:
            return

        border = "-" * (right-left)
        s.addstr(top, left, border)
        s.addstr(bottom, left, border)

        for y in range(top, bottom):
            s.addch(y, left, "|")
            s.addch(y, right, "|")

        s.addch(top, left, ",")
        s.addch(top, right, ".")
        s.addch(bottom, left, "`")
        s.addch(bottom, right, "'")

    def refresh(self):
        if self._key in ['\t', '\x10']:
            self._key = ""

        self._scr.refresh()


def wrapper(callback):
    curses.wrapper(UI(callback).start)
