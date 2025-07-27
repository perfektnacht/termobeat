import curses
from typing import List

from frames import OMARCHY_BANNER


class FlameParticle:
    """Represents a temporary flame emoji flying out from the center."""

    def __init__(self, angle: float, radius: float = 1.0, ttl: int = 4) -> None:
        self.angle = angle
        self.radius = radius
        self.ttl = ttl

    def update(self) -> None:
        """Advance the particle one step outward and reduce its life."""
        self.radius += 1
        self.ttl -= 1


def draw_frame(stdscr, amplitude, show_banner, slashes, user_radius, user_ttl, show_radius=False):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    center_y, center_x = height // 2, width // 2

    if show_banner:
        bottom_start = height - len(OMARCHY_BANNER)
        for i, line in enumerate(OMARCHY_BANNER):
            y = bottom_start + i
            x = (width - len(line)) // 2
            try:
                stdscr.addstr(y, x, line, curses.A_BOLD)
            except curses.error:
                continue

    for s in slashes:
        if 0 <= s.y < height and 0 <= s.x < width:
            try:
                stdscr.addstr(s.y, s.x, s.char, curses.A_BOLD)
            except curses.error:
                continue

    if show_radius:
        info = f"Slash TTL: {user_ttl} | Amplitude: {amplitude:.3f}"
        stdscr.addstr(1, (width - len(info)) // 2, info, curses.A_DIM)

    stdscr.refresh()
