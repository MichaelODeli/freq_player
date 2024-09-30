import dash_mantine_components as dmc


def render_freq_1_fields(freq_list):
    return dmc.Group(
        [
            dmc.Select(
                label="Номер частоты 1",
                data=[str(i) for i in freq_list.keys()],
                w=150,
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
                w=150,
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


def render_freq_buttons():
    return [
        dmc.Switch(
            size="md",
            radius="lg",
            label="Автовоспроизведение",
            checked=True,
            id="freq-autoplay",
        ),
        dmc.Switch(
            size="md",
            radius="lg",
            label="Подать сигнал модуляции перед передачей",
            checked=True,
            id="freq-modulation-play",
        ),
        dmc.Button(
            "Воспроизвести",
            id="freq-play",
            fullWidth=True,
        ),
        dmc.Group(
            id="freq-speak-modes",
            children=[
                dmc.Button(
                    "Нажать тангенту",
                    id="freq-tx",
                    w="40%",
                ),
                dmc.Button(
                    "Отпустить тангенту",
                    id="freq-rx",
                    w="40%",
                ),
            ],
            display="none",
            justify="space-between",
        ),
    ]
