import pyaudio
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100  # дискретизация


def generate_tone(
    frequency_duration_list, sample_rate=SAMPLE_RATE, return_separated_list=False
):
    """Generate tone by freq and time

    Args:
        frequency_duration_list (list): [frequency, duration]
        sample_rate (int, optional): Play sample rate. Defaults to SAMPLE_RATE.

    Returns:
        np.array: array with sound
    """
    if return_separated_list:
        full_wave = []
    else:
        full_wave = np.array([])  # Пустой массив для объединения всех волн

    for frequency, duration in frequency_duration_list:
        # Генерация звуковой волны для каждой частоты
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(2 * np.pi * frequency * t)

        # Объединяем звуки в один массив
        if return_separated_list:
            full_wave.append(list(wave))
        else:
            full_wave = np.concatenate((full_wave, wave))

    return full_wave


def play_tone(full_wave, sample_rate=SAMPLE_RATE):
    """Play tone from np.array

    Args:
        full_wave (np.array):
        sample_rate (int, optional): Play sample rate. Defaults to SAMPLE_RATE.
    """
    sd.play(full_wave, samplerate=sample_rate)
    sd.wait()  # Ожидание завершения воспроизведения
