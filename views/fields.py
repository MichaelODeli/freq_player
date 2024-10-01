import dash_mantine_components as dmc


def render_freq_1_fields(freq_list):
    return dmc.Group(
        [
            dmc.Select(
                label="Номер частоты 1",
                data=[str(i) for i in freq_list.keys()],
                w=250,
                id="freq-select-1",
                clearable=True,
            ),
            dmc.NumberInput(
                label="Частота 1, Гц",
                id="freq-1",
            ),
            dmc.NumberInput(
                label="Время подачи, мс",
                id="time-1",
            ),
        ]
    )


def render_freq_2_fields(freq_list):
    return dmc.Group(
        [
            dmc.Select(
                label="Номер частоты 2",
                data=[str(i) for i in freq_list.keys()],
                w=250,
                id="freq-select-2",
                clearable=True,
            ),
            dmc.NumberInput(
                label="Частота 2, Гц",
                id="freq-2",
            ),
            dmc.NumberInput(
                label="Время подачи, мс",
                id="time-2",
            ),
        ]
    )

def render_freq_3_fields(freq_list):
    return dmc.Group(
        [
            dmc.Select(
                label="Номер частоты 3",
                data=[str(i) for i in freq_list.keys()],
                w=250,
                id="freq-select-3",
                clearable=True,
            ),
            dmc.NumberInput(
                label="Частота 3, Гц",
                id="freq-3",
            ),
            dmc.NumberInput(
                label="Время подачи, мс",
                id="time-3",
            ),
        ]
    )


def render_freq_buttons():
    return [
        dmc.Button(
            "Воспроизвести",
            id="freq-play",
            fullWidth=True,
        ),
    ]
