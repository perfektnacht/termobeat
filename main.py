"""Main entry point for Termobeat.

The application captures audio amplitude using ``audio_input`` and
renders a metal inspired visualisation with curses. A simple beat
threshold spawns expanding wave animations and triggers the OMARCHY
banner. Each frame the amplitude, banner state and active waves are
passed to ``draw_frame`` for rendering.
"""

import curses
import time
from dataclasses import dataclass

# Default starting radius for new waves. Can be adjusted by user at runtime.
DEFAULT_RADIUS = 1
# Default time-to-live for new waves. Can be changed with [ and ] keys.
DEFAULT_TTL = 10

from audio_input import get_amplitude_band
from visualizer import draw_frame

# Configurable runtime constants
# Target frame rate of the curses UI
FPS = 30
# Minimum amplitude considered a beat
BEAT_THRESHOLD = 0.5  # Adjust this as needed


@dataclass
class Wave:
    """Represents an expanding wave spawned on each detected beat."""

    radius: int = 1
    ttl: int = DEFAULT_TTL

    def update(self) -> None:
        """Advance the wave by growing outward and counting down ``ttl``."""
        self.radius += 1
        self.ttl -= 1

    def is_alive(self) -> bool:
        """Return ``True`` while the wave still has time to live."""
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
    smoothed_amplitude = 0.0

    while True:
        amplitude = get_amplitude_band()
        smoothed_amplitude = (smoothed_amplitude * 0.9) + (amplitude * 0.1)

        key = stdscr.getch()
        if key == ord('+') or key == ord('='):
            user_radius = min(user_radius + 1, 10)
            message_timer = time.time()
        elif key == ord('-') or key == ord('_'):
            user_radius = max(user_radius - 1, 1)
            message_timer = time.time()
        elif key == ord(']'):
            user_ttl = min(user_ttl + 2, 30)
            message_timer = time.time()
        elif key == ord('['):
            user_ttl = max(user_ttl - 2, 2)
            message_timer = time.time()

        # Simple beat detection
        if amplitude > BEAT_THRESHOLD:
            show_banner = True
            last_beat_time = time.time()
            active_waves.append(Wave(radius=user_radius, ttl=user_ttl))

        if time.time() - last_beat_time > 0.3:
            show_banner = False

        # Update wave animations
        for wave in active_waves:
            wave.update()
        active_waves = [w for w in active_waves if w.is_alive()]

        draw_frame(
            stdscr,
            smoothed_amplitude,
            show_banner,
            active_waves,
            user_radius,
            user_ttl,
            show_radius=(time.time() - message_timer < 2),
        )
        time.sleep(1 / FPS)


if __name__ == "__main__":
    curses.wrapper(main)
