import pyaudio
import numpy as np

SAMPLE_RATE = 44100  # дискретизация
DURATION = 3  # секун

def get_default_output_device_index():
    p = pyaudio.PyAudio()
    try:
        default_device_index = p.get_default_output_device_info()["index"]
    except IOError:
        default_device_index = None
    p.terminate()
    return default_device_index


# sin генератор
def generate_tone(frequency, duration=DURATION):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)  # формула
    return tone.astype(np.float32)


def play_tone_versh(frequencies, callback=None):
    p = pyaudio.PyAudio()
    try:
        default_output_device_index = get_default_output_device_index()
        if default_output_device_index is None:
            raise OSError("No default output device found")
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=SAMPLE_RATE,
            output=True,
            output_device_index=default_output_device_index,
        )
        print(frequencies)
        for dur, frequency in frequencies:
            tone = generate_tone(frequency, dur)
            stream.write(tone)
        stream.stop_stream()
        stream.close()
        if callback:
            callback()
    except Exception as e:
        print(f"Error playing tone: {e}")
    finally:
        p.terminate()