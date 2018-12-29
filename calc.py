#!/usr/bin/env python3


import curses

import attr

import pycuil


@attr.s
class Button(object):
    x = attr.ib()
    y = attr.ib()
    label = attr.ib()


class CalcApp(object):
    """
    This is the quintessential hello-world type of app for any GUI,
    the humble 4-function calculator.

    This app is not intended to be useful, except insofar as to serve
    as a showcase/tutorial for how to use the Pycuil library.
    """

    def __init__(self):
        self.clear_all()

    def clear_all(self):
        self.accumulator = 0.0
        self.clear_display()

    def clear_display(self):
        self.readout = "0"

    def handle_key(self, k):
        if len(self.readout) < 15:
            if self.readout == "0":
                if k == '.':
                    self.readout = "0."
                else:
                    self.readout = k
            else:
                self.readout = self.readout + k

    def handle_op(self, k):
        value = float(self.readout)

        if k == '+':
            self.accumulator = self.accumulator + value
        if k == '-':
            self.accumulator = self.accumulator - value
        if k == '*':
            self.accumulator = self.accumulator * value
        if k == '/':
            if value == 0:
                self.accumulator = 0
                self.readout = 'err'
                return
            self.accumulator = self.accumulator / value
        self.readout = str(self.accumulator)

    def redraw(self):
        ui = self.ui

        ui.clear()

        self.done = ui.button(0, 2, "Q", "Q")

        if ui.button(8, 2, "C", "C"):
            self.clear_display()

        if ui.button(12, 2, "A", "A"):
            self.clear_all()

        for n in [
            Button(0, 4, '7'), Button(4, 4, '8'), Button(8, 4, '9'),
            Button(0, 5, '4'), Button(4, 5, '5'), Button(8, 5, '6'),
            Button(0, 6, '1'), Button(4, 6, '2'), Button(8, 6, '3'),
            Button(0, 7, '0'), Button(4, 7, '.'),
        ]:
            if ui.button(n.x, n.y, n.label, n.label) and self.readout != 'err':
                self.handle_key(n.label)

        for op in [
            Button(12, 4, '+'),
            Button(12, 5, '-'),
            Button(12, 6, '*'),
            Button(12, 7, '/'),
        ]:
            if ui.button(op.x, op.y, op.label, op.label) and self.readout != 'err':
                self.handle_op(op.label)

        ui.label(0, 0, (("_"*15)+self.readout)[-15:])
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
    pycuil.wrapper(CalcApp().start)
