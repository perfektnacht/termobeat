import curses
import math
from typing import List

from frames import OMARCHY_BANNER
from utils import draw_top_centered_text


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


def draw_frame(
    stdscr,
    amplitude: float,
    waves: List["Wave"],
    flames: List[FlameParticle],
    user_radius: int,
    user_ttl: int,
    show_radius: bool = False,
) -> None:
    """Draw a single visualization frame."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    center_y, center_x = height // 2, width // 2

    # Draw OMARCHY banner fixed at the top center
    for i, line in enumerate(OMARCHY_BANNER):
        draw_top_centered_text(stdscr, line, y=1 + i, attr=curses.A_BOLD)

    # Draw flame particles
    for flame in flames:
        y = center_y + int(round(math.sin(flame.angle) * flame.radius))
        x = center_x + int(round(math.cos(flame.angle) * flame.radius))
        try:
            stdscr.addstr(y, x, "\U0001F525")  # flame emoji
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
