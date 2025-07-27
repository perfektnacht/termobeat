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

    radius: int = 0

    def update(self) -> None:
        """Advance the wave animation by one step by growing its radius."""
        self.radius += 1

    def active(self, max_radius: int = 6) -> bool:
        """Return ``True`` while ``radius`` is not beyond ``max_radius``."""
        return self.radius <= max_radius


def main(stdscr: curses.window) -> None:
    """Run the curses application main loop."""
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()

    last_beat_time = 0.0
    show_banner = False
    active_waves: list[Wave] = []

    while True:
        amplitude = get_amplitude_band()

        # Simple beat detection
        if amplitude > BEAT_THRESHOLD:
            show_banner = True
            last_beat_time = time.time()
            active_waves.append(Wave())

        if time.time() - last_beat_time > 0.3:
            show_banner = False

        # Update wave animations
        for wave in active_waves:
            wave.update()
        active_waves = [w for w in active_waves if w.active()]

        draw_frame(stdscr, amplitude, show_banner, active_waves)
        time.sleep(1 / FPS)


if __name__ == "__main__":
    curses.wrapper(main)
