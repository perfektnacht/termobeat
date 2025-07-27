import curses
from frames import OMARCHY_BANNER

# Pre-compute the banner width so each line can be aligned consistently.
BANNER_WIDTH = max(len(line) for line in OMARCHY_BANNER)


def draw_frame(stdscr, amplitude, slashes, user_ttl, show_radius=False):
    """Draw the current frame for the visualizer."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    omarchy_y = height - len(OMARCHY_BANNER) - 1
    banner_x = (width - BANNER_WIDTH) // 2

    # Draw slashes falling through the entire screen area
    # Allow slashes to fall nearly to the bottom, stopping above the banner
    mid_y = height - len(OMARCHY_BANNER) - 2
    for s in slashes:
        if 0 <= s.y < mid_y and 0 <= s.x < width:
            try:
                stdscr.addstr(s.y, s.x, s.char, curses.A_BOLD)
            except curses.error:
                continue

    # Draw static OMARCHY banner centered at the bottom of the screen
    for i, line in enumerate(OMARCHY_BANNER):
        y = omarchy_y + i
        try:
            stdscr.addstr(y, banner_x, line, curses.A_BOLD)
        except curses.error:
            continue

    # HUD info
    if show_radius:
        info = f"Slash TTL: {user_ttl} | Amplitude: {amplitude:.3f}"
        stdscr.addstr(1, (width - len(info)) // 2, info, curses.A_DIM)

    stdscr.refresh()
