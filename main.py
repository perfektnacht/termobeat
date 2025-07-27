"""Main entry point for Termobeat."""

import curses
import time
import random

from audio_input import get_amplitude_band
from visualizer import draw_frame

# Target frame rate of the curses UI
FPS = 30
# Minimum amplitude considered a beat
BEAT_THRESHOLD = 0.03  # Lowered for better sensitivity

# Default starting values for user controlled wave properties
DEFAULT_RADIUS = 3
DEFAULT_TTL = 20


class Slash:
    def __init__(self, x, y, char, ttl=8):
        self.x = x
        self.y = y
        self.char = char
        self.ttl = ttl

    def update(self):
        self.y += 1  # Move down
        self.ttl -= 1

    def is_alive(self):
        return self.ttl > 0


def main(stdscr: curses.window) -> None:
    """Run the curses application main loop."""
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()

    active_slashes: list[Slash] = []
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
            num_slashes = int(amplitude * 100)  # spawn more if louder
            for _ in range(num_slashes):
                x = random.randint(0, curses.COLS - 1)
                y = 0
                char = random.choice(['|', '/', '\\'])
                active_slashes.append(Slash(x, y, char, ttl=user_ttl))

        for slash in active_slashes:
            slash.update()
        active_slashes = [s for s in active_slashes if s.is_alive()]

        draw_frame(
            stdscr,
            amplitude,
            amplitude > BEAT_THRESHOLD,
            active_slashes,
            user_radius,
            user_ttl,
            show_radius=(time.time() - message_timer < 2),
        )

        time.sleep(1 / FPS)


if __name__ == "__main__":
    curses.wrapper(main)
