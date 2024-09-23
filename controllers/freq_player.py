from controllers import freq_maker
import threading

def play(freq_1, freq_2, time_1, time_2, return_vals=False):
    freq_lst = [[freq_1, time_1 / 1000], [freq_2, time_2 / 1000]]
    full_wave = freq_maker.generate_tone(freq_lst)
    threading.Thread(target=freq_maker.play_tone, args=([full_wave])).start()

    if return_vals:
        return freq_lst, full_wave