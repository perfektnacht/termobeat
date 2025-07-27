import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024
CHANNELS = 1
last_amplitude = 0.0

def find_preferred_device():
    devices = sd.query_devices()

    # Try to find loopback / monitor
    for i, dev in enumerate(devices):
        name = dev['name'].lower()
        if "monitor" in name or "loopback" in name:
            if dev['max_input_channels'] >= 1:
                print(f"✅ Using loopback device: {dev['name']}")
                return i

    # Fallback to default mic
    print("⚠️  No loopback found. Falling back to default input device.")
    return None  # Use system default

def audio_callback(indata, frames, time, status):
    global last_amplitude
    if status:
        print(status)

    mono_data = indata[:, 0]
    fft_result = np.abs(np.fft.rfft(mono_data))
    fft_norm = fft_result / np.sum(fft_result + 1e-8)

    band_energy = np.mean(fft_norm[5:30])
    last_amplitude = min(max(band_energy * 10, 0), 1)

def get_amplitude_band():
    global last_amplitude
    return last_amplitude

# Choose device
DEVICE_INDEX = find_preferred_device()

# Start the stream
stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    channels=CHANNELS,
    callback=audio_callback,
    device=DEVICE_INDEX
)
stream.start()
