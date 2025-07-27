"""Main entry point for Termobeat."""

import curses
import time

from audio_input import get_amplitude_band
from visualizer import draw_frame

# Target frame rate of the curses UI
FPS = 30
# Minimum amplitude considered a beat
BEAT_THRESHOLD = 0.03  # Lowered for better sensitivity

# Default starting values for user controlled wave properties
DEFAULT_RADIUS = 3
DEFAULT_TTL = 10


class Wave:
    """Represents an expanding ring spawned on each beat."""

    def __init__(self, radius: int = 1, ttl: int = 10) -> None:
        self.radius = radius
        self.ttl = ttl

    def update(self) -> None:
        """Grow the ring outward and decrease its remaining life."""
        self.radius += 1
        self.ttl -= 1

    def is_alive(self) -> bool:
        """Return ``True`` while the wave should still be drawn."""
        return self.ttl > 0


def main(stdscr: curses.window) -> None:
    """Run the curses application main loop."""
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()

    last_beat_time = 0.0
    show_banner = False
    active_waves: list[Wave] = []
    user_radius = DEFAULT_RADIUS
    user_ttl = DEFAULT_TTL
    message_timer = 0.0

    while True:
        amplitude = get_amplitude_band()
        key = stdscr.getch()

        if key == ord("+") or key == ord("="):
            user_radius = min(user_radius + 1, 10)
            message_timer = time.time()
        elif key == ord("-") or key == ord("_"):
            user_radius = max(user_radius - 1, 1)
            message_timer = time.time()
        elif key == ord("]"):
            user_ttl = min(user_ttl + 2, 30)
            message_timer = time.time()
        elif key == ord("["):
            user_ttl = max(user_ttl - 2, 2)
            message_timer = time.time()

        if amplitude > BEAT_THRESHOLD:
            show_banner = True
            last_beat_time = time.time()
            active_waves.append(Wave(radius=user_radius, ttl=user_ttl))

        if time.time() - last_beat_time > 0.3:
            show_banner = False

        for wave in active_waves:
            wave.update()
        active_waves = [w for w in active_waves if w.is_alive()]

        draw_frame(
            stdscr,
            amplitude,
            show_banner,
            active_waves,
            user_radius,
            user_ttl,
            show_radius=(time.time() - message_timer < 2),
        )

        time.sleep(1 / FPS)


if __name__ == "__main__":
    curses.wrapper(main)
