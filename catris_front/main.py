import curses
import signal
import time
from game import Game


TPS = 20
BLOCK_WIDTH = 2
BLOCK_HEIGHT = 1 


def resize(stdscr, window):
    curses.endwin()
    stdscr.refresh()
    window.clear()
    window.refresh()
    stdscr.nodelay(True)
    rows, cols = stdscr.getmaxyx()
    window.resize(rows, cols)
    window.mvwin(0, 0)
    return window


def draw_borders(window):
    rows, cols = window.getmaxyx()
    for y in [0, rows - 1]:
        for x in range(1, cols - 1):
            window.addch(y, x, curses.ACS_HLINE)

    for x in [0, cols - 1]:
        for y in range(1, rows - 1):
            window.addch(y, x, curses.ACS_VLINE)

    window.addch(0, 0, curses.ACS_ULCORNER)
    window.addch(0, cols - 1, curses.ACS_URCORNER)
    window.addch(rows - 1, 0, curses.ACS_LLCORNER)
    window.insch(rows - 1, cols - 1, curses.ACS_LRCORNER)


def main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.refresh()
    stdscr.nodelay(True)
    curses.start_color()
    curses.curs_set(0)

    # Create a windows as large as the screen
    window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
    signal.signal(signal.SIGWINCH, lambda signal, frame: resize(stdscr, window))

    game = Game()
    last_tick_time = time.time()
    pressed_keys = set()

    while True:
        while (key := stdscr.getch()) != -1:
            pressed_keys.add(key)

        tick_time = time.time()
        if tick_time < 1 / TPS + last_tick_time:
            continue

        last_tick_time = tick_time
        game.tick(pressed_keys)
        pressed_keys.clear()

        # Redraw the screen.
        window.clear()
        draw_borders(window)
        game.draw(BLOCK_HEIGHT, BLOCK_WIDTH, window)
        
        window.refresh()


curses.wrapper(main)
