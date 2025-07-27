import curses
from frames import OMARCHY_BANNER, HAND_FRAMES


def draw_frame(stdscr, amplitude, show_banner):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Draw hand based on amplitude level
    if amplitude > 0.6:
        hand = HAND_FRAMES[1]
    elif amplitude > 0.3:
        hand = HAND_FRAMES[0]
    else:
        hand = HAND_FRAMES[2]

    for i, line in enumerate(hand):
        x = (width - len(line)) // 2
        y = height // 2 + i
        stdscr.addstr(y, x, line)

    # Draw OMARCHY banner on beat
    if show_banner:
        for i, line in enumerate(OMARCHY_BANNER):
            x = (width - len(line)) // 2
            y = height // 2 - len(OMARCHY_BANNER) + i - 2
            stdscr.addstr(y, x, line, curses.A_BOLD)

    stdscr.refresh()
