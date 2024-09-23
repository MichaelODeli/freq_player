import pyaudio
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100  # дискретизация

def play_tones(frequency_duration_list, sample_rate=SAMPLE_RATE):
    """
    Воспроизводит звуки указанных частот и длительности последовательно без пауз.

    :param frequency_duration_list: список формата [[frequency, duration], ...], 
    :param sample_rate: частота дискретизации (по умолчанию 44100 Гц).
    :return sound:
    """
    full_wave = np.array([])  # Пустой массив для объединения всех волн

    for frequency, duration in frequency_duration_list:
        # Генерация звуковой волны для каждой частоты
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(2 * np.pi * frequency * t)

        # Объединяем звуки в один массив
        full_wave = np.concatenate((full_wave, wave))
    
    # Воспроизведение объединённой звуковой волны
    sd.play(full_wave, samplerate=sample_rate)
    sd.wait()  # Ожидание завершения воспроизведения