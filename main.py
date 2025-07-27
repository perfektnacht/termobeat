import curses
import time
from audio_input import get_amplitude_band
from visualizer import draw_frame

FPS = 30
BEAT_THRESHOLD = 0.5  # Adjust this as needed

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()

    last_beat_time = 0
    show_banner = False

    while True:
        # Get amplitude from audio
        amplitude = get_amplitude_band()

        # Simple beat detection
        if amplitude > BEAT_THRESHOLD:
            show_banner = True
            last_beat_time = time.time()

        # Hide banner after 300ms
        if time.time() - last_beat_time > 0.3:
            show_banner = False

        draw_frame(stdscr, amplitude, show_banner)

        time.sleep(1 / FPS)

if __name__ == '__main__':
    curses.wrapper(main)
