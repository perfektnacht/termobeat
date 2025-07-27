"""Audio input utilities for Termobeat using sounddevice.

This module captures the current amplitude from the system's audio
output. It does so by opening a sounddevice ``InputStream`` in loopback
mode. A loopback device routes whatever is being played on the speakers
back into an input so we can analyse it like a microphone.

Operating system support varies:

* **Linux** typically exposes monitor sources through PulseAudio/ALSA
  which contain ``monitor`` in their device name.
* **Windows** may offer "Stereo Mix" or similar loopback-capable inputs.
* **macOS** requires third party tools (e.g. BlackHole or Soundflower)
  to create a virtual loopback device.

When imported the module automatically starts an ``InputStream`` using
such a device, storing recent amplitudes so ``get_amplitude_band`` can be
called by the rest of the application.
"""

import numpy as np
import sounddevice as sd

# Constants controlling the capture parameters
# Standard CD-quality sample rate in hertz
SAMPLE_RATE = 44100
# Number of samples per audio block processed in the callback
BLOCK_SIZE = 1024
# We only care about a single channel (mono)
CHANNELS = 1

_current_amplitude = 0.0


def find_loopback_device() -> int:
    """Return an input device index suitable for loopback recording.

    The function searches the available devices for names that usually
    indicate loopback capability such as ``monitor`` or ``stereo mix``.
    ``None`` is returned if no matching device is found.
    """
    devices = sd.query_devices()
    for idx, dev in enumerate(devices):
        name = dev.get("name", "").lower()
        if dev.get("max_input_channels", 0) > 0 and (
            "monitor" in name or "loopback" in name or "stereo mix" in name
        ):
            return idx
    return None


def audio_callback(indata, frames, time, status):
    """Store the root mean square amplitude of the incoming block."""
    global _current_amplitude
    if status:
        # status is printed to stderr by sounddevice when non-empty
        pass
    # Compute RMS amplitude of the mono signal
    amplitude = np.sqrt(np.mean(indata**2))
    _current_amplitude = float(amplitude)


# Initialize the input stream on import
_device = find_loopback_device()
if _device is None:
    raise RuntimeError(
        "No loopback-capable input device found. See module documentation "
        "for platform specific requirements."
    )

stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    channels=CHANNELS,
    callback=audio_callback,
    device=_device,
)
stream.start()


def get_amplitude_band() -> float:
    """Return the last measured amplitude of the loopback audio stream."""
    return _current_amplitude

