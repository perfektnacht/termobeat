# termobeat

CLI based audio analyzer with a metal twist.

## Requirements

- Python 3.9 or higher
- Packages listed in `requirements.txt`

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Loopback audio device

Termobeat captures whatever is currently playing on your speakers by opening a loopback recording device. Linux often exposes devices containing `monitor` in the name. Windows may offer "Stereo Mix" and macOS typically requires a third‑party driver like BlackHole or Soundflower. Make sure such a device is available, otherwise the program fails at startup.

## Usage

Run the program from a terminal that supports the `curses` library:

```bash
python main.py
```

Press `Ctrl+C` to exit.

### Controls

Use the following keys at runtime:

- `[` / `]` to change how long spawned slashes stay on screen.
