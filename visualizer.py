"""Curses based rendering helpers for Termobeat.

The drawing routines consume the ASCII art defined in ``frames`` and
render it to a ``curses`` window based on the current audio amplitude.
"""

import curses
from frames import OMARCHY_BANNER, HAND_FRAMES, WAVE_TEMPLATE


def draw_frame(
    stdscr: curses.window,
    amplitude: float,
    show_banner: bool,
    active_waves,
    user_radius: int,
    user_ttl: int,
    show_radius: bool = False,
):
    """Render a single frame to ``stdscr``.

    Parameters
    ----------
    stdscr : curses.window
        Window where drawing occurs.
    amplitude : float
        Current audio amplitude in the ``[0, 1]`` range.
    show_banner : bool
        Whether the OMARCHY banner should be displayed.
    active_waves : Sequence[Wave]
        List of expanding wave animations. Older waves are drawn first.

    user_ttl : int
        Time-to-live in frames for newly spawned waves.

    Rendering order is waves, then the hand, then the banner. If ``show_radius``
    is ``True`` a status message with the current wave radius and TTL is
    displayed.
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    center_y = height // 2
    center_x = width // 2
    # 1. Draw expanding waves triggered by beats
    for wave in active_waves:
        ring_top = center_y - len(WAVE_TEMPLATE) // 2 - wave.radius
        ring_left = center_x - len(WAVE_TEMPLATE[0]) // 2 - wave.radius
        for i, line in enumerate(WAVE_TEMPLATE):
            y = ring_top + i
            x = ring_left
            try:
                stdscr.addstr(y, x, line)
            except curses.error:
                # Ignore attempts to draw outside the screen bounds
                pass

    # 2. Draw hand based on amplitude level
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

    # 3. Draw OMARCHY banner on beat
    if show_banner:
        for i, line in enumerate(OMARCHY_BANNER):
            x = (width - len(line)) // 2
            y = height // 2 - len(OMARCHY_BANNER) + i - 2
            stdscr.addstr(y, x, line, curses.A_BOLD)

    if show_radius:
        radius_msg = f"Wave Radius: {user_radius} | TTL: {user_ttl}"
        stdscr.addstr(1, (width - len(radius_msg)) // 2, radius_msg, curses.A_DIM)

    stdscr.refresh()
