import numpy as np
import plotly.graph_objects as go

def get_fig(freq_lst, full_wave, scale_factor=75):
    full_wave = np.interp(
        np.arange(0, len(full_wave), scale_factor),
        np.arange(0, len(full_wave)),
        full_wave,
    )

    fig = go.Figure()
    dur_sum = 0
    prev_limit = 0
    for frequency, duration in freq_lst:
        dur_sum += duration
        element_counter = int(
            (duration / sum([b for a, b in freq_lst])) * len(full_wave)
        )

        fig.add_scatter(
            x=[prev_limit + i for i in range(element_counter)],
            y=full_wave[prev_limit : prev_limit + element_counter],
            name=f"f = {frequency} Hz, t = {int(duration*1000)} ms",
        )
        prev_limit += element_counter

    fig.update_layout(
        title="График проигранного сигнала",
        xaxis_title="t, ms",
        legend_title="Сигналы",
    )
    return fig
