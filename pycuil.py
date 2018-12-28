# PyCUIL -- Python Console User Interface Library


import curses

import attr


@attr.s
class UI(object):
    mainloop = attr.ib()
    _scr = attr.ib(init=None, default=None)
    _key = attr.ib(init=None, default="")


    def start(self, stdscr):
        """
        Initialize the underlying console drawing API (be it ncurses or
        whatever else is supported), then kick off the application's mainloop.
        """
        self._scr = stdscr
        self.mainloop(self)

    def wait_event(self):
        """
        Waits for an event at the keyboard.  The received keycode will be cached
        for later use by the application's mainloop.
        """
        self._key = self._scr.getkey()


    def button(self, x, y, label, hotkey):
        """
        Render a button on the screen.

        Returns True if the button is activated, either by the hotkey provided
        or through some other reasonable means.  If no hotkey is desired,
        provide None.  Otherwise, any curses-compatible string representation
        can be used (e.g., `^G` for CTRL-G, `KEY_F(1)` for F1, etc.).
        """

        s = self._scr

        # Draw the button
        s.addstr(y, x, "[{}]".format(label))

        # The button was activated via hotkey
        if hotkey and (hotkey == self._key):
            self._key = ""
            return True

    def label(self, x, y, string):
        """
        Render a plain string.  Labels cannot be activated.
        """
        self._scr.addstr(y, x, string)

    def refresh(self):
        self._scr.refresh()


def wrapper(callback):
    curses.wrapper(UI(callback).start)
