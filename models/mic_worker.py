import sounddevice as sd

def mic_to_speaker(sample_rate=44100, block_size=1024):
    """
    Захватывает аудио с микрофона и передаёт его на динамики в режиме реального времени.
    
    sample_rate: частота дискретизации (по умолчанию 44100 Гц).
    block_size: размер блока данных для буферизации (по умолчанию 1024).
    """
    def callback(indata, outdata, frames, time, status):
        if status:
            print(f"Статус ошибки: {status}", flush=True)
        outdata[:] = indata  # Передача аудиоданных с микрофона на динамики

    # Создаем аудиопоток с захватом и выводом аудио
    try:
        with sd.Stream(channels=1, samplerate=sample_rate, blocksize=block_size, callback=callback):
            print("Нажмите Ctrl+C для завершения...")
            while True:
                sd.sleep(100)  # Задержка, чтобы не загружать процессор
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск функции
mic_to_speaker()
