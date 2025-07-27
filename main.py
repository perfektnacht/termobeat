"""Main entry point for Termobeat."""

import curses
import time
import math
import random

from audio_input import get_amplitude_band
from visualizer import draw_frame, FlameParticle

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

    active_waves: list[Wave] = []
    active_flames: list[FlameParticle] = []
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
            active_waves.append(Wave(radius=user_radius, ttl=user_ttl))
            for _ in range(8):
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(4, 6)
                active_flames.append(FlameParticle(angle, radius, ttl=4))

        for wave in active_waves:
            wave.update()
        active_waves = [w for w in active_waves if w.is_alive()]
        for flame in active_flames:
            flame.update()
        active_flames = [f for f in active_flames if f.ttl > 0]

        draw_frame(
            stdscr,
            amplitude,
            active_waves,
            active_flames,
            user_radius,
            user_ttl,
            show_radius=(time.time() - message_timer < 2),
        )

        time.sleep(1 / FPS)


if __name__ == "__main__":
    curses.wrapper(main)
