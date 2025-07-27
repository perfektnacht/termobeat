import curses
from frames import OMARCHY_BANNER


def draw_frame(stdscr, amplitude, slashes, user_ttl, show_radius=False):
    """Draw the current frame for the visualizer."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    omarchy_y = height - len(OMARCHY_BANNER) - 1
    center_x = width // 2

    # Draw slashes falling from the top down to just above the OMARCHY banner
    for s in slashes:
        if 0 <= s.y < omarchy_y and 0 <= s.x < width:
            try:
                stdscr.addstr(s.y, s.x, s.char, curses.A_BOLD)
            except curses.error:
                continue

    # Draw static OMARCHY banner centered at the bottom of the screen
    for i, line in enumerate(OMARCHY_BANNER):
        y = omarchy_y + i
        x = (width - len(line)) // 2
        try:
            stdscr.addstr(y, x, line, curses.A_BOLD)
        except curses.error:
            continue

    # HUD info
    if show_radius:
        info = f"Slash TTL: {user_ttl} | Amplitude: {amplitude:.3f}"
        stdscr.addstr(1, (width - len(info)) // 2, info, curses.A_DIM)

    stdscr.refresh()
