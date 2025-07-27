import curses
import math
from frames import OMARCHY_BANNER


def draw_frame(stdscr, amplitude, show_banner, waves, user_radius, user_ttl, show_radius=False):
    """Draw a single visualization frame."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    center_y, center_x = height // 2, width // 2

    # Draw OMARCHY banner
    if show_banner:
        for i, line in enumerate(OMARCHY_BANNER):
            y = center_y - len(OMARCHY_BANNER) + i - 2
            x = (width - len(line)) // 2
            try:
                stdscr.addstr(y, x, line, curses.A_BOLD)
            except curses.error:
                continue

    # Draw waves
    for wave in waves:
        draw_wave_ring(stdscr, center_y, center_x, wave.radius)

    # Display radius and TTL settings
    if show_radius:
        info = f"Wave Radius: {user_radius} | TTL: {user_ttl}"
        stdscr.addstr(1, (width - len(info)) // 2, info, curses.A_DIM)

    # Display live amplitude
    amp_display = f"Amplitude: {amplitude:.3f}"
    stdscr.addstr(0, 2, amp_display, curses.A_DIM)

    stdscr.refresh()


def draw_wave_ring(stdscr, cy, cx, radius):
    """Draw a circular ring of ``radius`` around (cx, cy)."""
    char = '█' if radius < 5 else '*'
    points = 32
    for i in range(points):
        angle = 2 * math.pi * i / points
        dx = int(round(math.cos(angle) * radius))
        dy = int(round(math.sin(angle) * radius))
        y, x = cy + dy, cx + dx
        try:
            stdscr.addstr(y, x, char, curses.A_BOLD)
        except curses.error:
            continue
