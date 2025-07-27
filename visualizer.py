import curses
from frames import OMARCHY_BANNER, HAND_FRAMES, WAVE_TEMPLATE


def draw_frame(stdscr, amplitude, show_banner, active_waves):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    center_y = height // 2
    # Draw expanding waves triggered by beats
    for wave in active_waves:
        for i, line in enumerate(WAVE_TEMPLATE):
            y = center_y - wave.radius + i - 3
            x = (width - len(line)) // 2
            try:
                stdscr.addstr(y, x, line)
            except curses.error:
                pass

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
