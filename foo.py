#!/usr/bin/env python3


import curses
import time


def main(stdscr):
    stdscr.clear()

    for i in range(0, 11):
        v = i + 10
        stdscr.addstr(i, i*10, '10 divided by {} is {}'.format(v, 10/v))

#   stdscr.refresh()
    stdscr.addstr('{}'.format(stdscr.getkey()))
    stdscr.refresh()
    time.sleep(10)


if __name__ == '__main__':
    curses.wrapper(main)
