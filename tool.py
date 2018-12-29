#!/usr/bin/env python3


import attr

import pycuil


@attr.s
class Button(object):
    x = attr.ib()
    y = attr.ib()
    label = attr.ib()


class ToolApp(object):
    def __init__(self):
        self.words = [0] * 16

    def redraw(self):
        ui = self.ui

        ui.clear()

        ui.label(1, 1, "HEX")
        ui.frame(0, 2, 7, 19)
        for i, w in enumerate(self.words):
            ui.label(2, 3+i, "{:04X}".format(w))


        ui.label(11, 1, "ADDRESS RANGE")
        ui.frame(10, 2, 17, 4)
        ui.label(12, 3, "0090")

        ui.label(18, 3, "--")

        ui.frame(20, 2, 27, 4)
        ui.label(22, 3, "009F")

        ui.button(0, 23, " Apply ", "A")
        self.done = ui.button(11, 23, " Quit ", "Q")

        ui.refresh()

    def start(self, ui):
        self.ui = ui
        self.done = False

        while True:
            self.redraw()
            if self.done:
                break
            ui.wait_event()


if __name__ == '__main__':
    pycuil.wrapper(ToolApp().start)
