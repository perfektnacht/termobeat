"""Helper functions for drawing with curses."""

import curses


def center_text(stdscr: curses.window, text: str, y_offset: int = 0, attr: int = 0) -> None:
    """Draw ``text`` centered on ``stdscr``.

    Parameters
    ----------
    stdscr : curses.window
        The window to draw on.
    text : str
        Text to display.
    y_offset : int, optional
        Vertical offset from the center line.
    attr : int, optional
        Additional attributes such as ``curses.A_BOLD``.
    """
    height, width = stdscr.getmaxyx()
    x = (width - len(text)) // 2
    y = height // 2 + y_offset
    stdscr.addstr(y, x, text, attr)


def init_colors() -> int:
    """Initialize a single red color pair and return its attribute."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    return curses.color_pair(1)
