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


def draw_top_centered_text(stdscr: curses.window, text: str, y: int = 1, attr: int = curses.A_BOLD) -> None:
    """Draw ``text`` centered horizontally near the top of ``stdscr``.

    Parameters
    ----------
    stdscr : curses.window
        The window to draw on.
    text : str
        Text to display.
    y : int, optional
        The row from the top where text should be drawn.
    attr : int, optional
        Additional attributes such as ``curses.A_BOLD``.
    """
    height, width = stdscr.getmaxyx()
    x = max((width - len(text)) // 2, 0)
    if 0 <= y < height:
        try:
            stdscr.addstr(y, x, text, attr)
        except curses.error:
            pass
