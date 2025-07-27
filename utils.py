import curses


def center_text(stdscr, text, y_offset=0, attr=0):
    """Helper to draw centered text on the screen."""
    height, width = stdscr.getmaxyx()
    x = (width - len(text)) // 2
    y = height // 2 + y_offset
    stdscr.addstr(y, x, text, attr)


def init_colors():
    """Initialize color pairs and return a basic color attribute."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    return curses.color_pair(1)
