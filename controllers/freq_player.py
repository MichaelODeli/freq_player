from controllers import freq_maker
import threading

def play_2(freq_1, freq_2, time_1, time_2, return_vals=False):
    freq_lst = [[freq_1, time_1 / 1000], [freq_2, time_2 / 1000]]
    full_wave = freq_maker.generate_tone(freq_lst)
    threading.Thread(target=freq_maker.play_tone, args=([full_wave])).start()

    if return_vals:
        return freq_lst, full_wave

def play_3(freq_1, freq_2, freq_3, time_1, time_2, time_3, return_vals=False):
    freq_lst = [[freq_1, time_1 / 1000], [freq_2, time_2 / 1000], [freq_3, time_3 / 1000]]
    full_wave = freq_maker.generate_tone(freq_lst)
    threading.Thread(target=freq_maker.play_tone, args=([full_wave])).start()

    if return_vals:
        return freq_lst, full_wave