import threading

import dash
import dash_mantine_components as dmc
import flask
from dash import Input, Output, State, dcc, html, no_update
from dash_iconify import DashIconify

import styles
from freq_maker import play_tone_versh

dash._dash_renderer._set_react_version("18.2.0")


def get_icon(icon):
    return DashIconify(icon=icon, height=20)


# flask and dash configuration
server = flask.Flask("PlaySound")
app = dash.Dash(
    "PlaySound",
    server=server,
    # use_pages=True,
    external_stylesheets=styles.STYLESHEETS,
    title="PlaySound",
    update_title="PlaySound 🔃",
    suppress_callback_exceptions=True,
)

freq_list = {
    # 'Не указано': None,
    2: 1071,
    6: 1207,
    7: 1241,
    9: 1309,
    12: 1411,
    14: 1479,
    16: 1547,
    17: 1581,
    19: 1649,
    20: 1683,
    36: 2227,
    38: 2295,
}


# Конструкция всего макета
app.layout = dmc.MantineProvider(
    children=[
        dmc.AppShell(
            [
                dmc.AppShellNavbar(
                    children=dmc.Stack(
                        [
                            dmc.NavLink(
                                label="Очистить частоты",
                                id="freq-clear",
                                leftSection=get_icon(icon="mdi:clear"),
                            ),
                            dmc.NavLink(
                                label='Режим "Прием"',
                                description="Отпустить тангенту",
                                id="freq-priem",
                                leftSection=get_icon(
                                    icon="material-symbols:call-received"
                                ),
                            ),
                            dmc.NavLink(
                                label='Режим "Передача"',
                                description="Нажать тангенту",
                                id="freq-pered",
                                leftSection=get_icon(icon="material-symbols:call-made"),
                            ),
                            dmc.NavLink(
                                label='Вызов "ЛОК"',
                                id="freq-call-loc",
                                leftSection=get_icon(icon="solar:call-cancel-outline"),
                                disabled=True,
                            ),
                            dmc.NavLink(
                                label="Отбой",
                                id="freq-otboy",
                                leftSection=get_icon(icon="solar:call-cancel-outline"),
                            ),
                            dmc.NavLink(
                                label="Контроль",
                                id="freq-control",
                                leftSection=get_icon(icon="mdi:user-access-control"),
                            ),
                        ],
                        align="center",
                        pt="sm",
                        gap=0,
                    ),
                ),
                dmc.AppShellMain(
                    dmc.Stack(
                        [
                            dmc.Group(
                                [
                                    dmc.Select(
                                        label="Номер частоты 1",
                                        data=[str(i) for i in freq_list.keys()],
                                        w=150,
                                        id="freq-select-1",
                                        clearable=True,
                                    ),
                                    dmc.NumberInput(label="Частота 1, Гц", id="freq-1"),
                                    dmc.NumberInput(
                                        label="Время подачи, мс",
                                        id="time-1",
                                    ),
                                ]
                            ),
                            dmc.Group(
                                [
                                    dmc.Select(
                                        label="Номер частоты 2",
                                        data=[str(i) for i in freq_list.keys()],
                                        w=150,
                                        id="freq-select-2",
                                        clearable=True,
                                    ),
                                    dmc.NumberInput(label="Частота 2, Гц", id="freq-2"),
                                    dmc.NumberInput(
                                        label="Время подачи, мс", id="time-2"
                                    ),
                                ]
                            ),
                            dmc.Switch(
                                size="md",
                                radius="lg",
                                label="Автовоспроизведение частоты при нажатии параметра",
                                checked=False,
                                id="freq-autoplay",
                                disabled=True,
                            ),
                            dmc.Button("Воспроизвести", id="freq-play", fullWidth=True),
                            html.Div(id="play-results"),
                        ],
                        px="sm",
                        pt="sm",
                        w="max-content",
                        gap="lg",
                    ),
                ),
            ],
            navbar={
                "width": 230,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
        ),
        dmc.NotificationProvider(position="bottom-right"),
        html.Div(id="notifications-container"),
    ],
    defaultColorScheme="light",
    theme={
        "primaryColor": styles.PRIMARY_COLOR,
        "fontFamily": styles.FONT_FAMILY,
        "headings": styles.HEADINGS,
        "colors": styles.COLORS,
    },
)


@app.callback(
    Output("freq-select-1", "value", allow_duplicate=True),
    Output("freq-select-2", "value", allow_duplicate=True),
    Input("freq-otboy", "n_clicks"),
    prevent_initial_call=True,
)
def set_freq_otboy(n_clicks):
    return ["2", "6"] if n_clicks is not None else [no_update, no_update]


@app.callback(
    Output("freq-select-1", "value", allow_duplicate=True),
    Output("freq-select-2", "value", allow_duplicate=True),
    Input("freq-control", "n_clicks"),
    prevent_initial_call=True,
)
def set_freq_control(n_clicks):
    return ["6", "2"] if n_clicks is not None else [no_update, no_update]


@app.callback(
    Output("freq-1", "value", allow_duplicate=True),
    Output("time-1", "value", allow_duplicate=True),
    Output("freq-2", "value", allow_duplicate=True),
    Output("time-2", "value", allow_duplicate=True),
    Input("freq-priem", "n_clicks"),
    prevent_initial_call=True,
)
def set_freq_listen(n_clicks):
    return (
        [freq_list[38], 200, freq_list[36], 200] if n_clicks is not None else [""] * 4
    )


@app.callback(
    Output("freq-1", "value", allow_duplicate=True),
    Output("time-1", "value", allow_duplicate=True),
    Output("freq-2", "value", allow_duplicate=True),
    Output("time-2", "value", allow_duplicate=True),
    Input("freq-pered", "n_clicks"),
    prevent_initial_call=True,
)
def set_freq_send(n_clicks):
    return (
        [freq_list[36], 200, freq_list[38], 200] if n_clicks is not None else [""] * 4
    )


@app.callback(
    Output("freq-1", "value", allow_duplicate=True),
    Output("time-1", "value", allow_duplicate=True),
    Input("freq-select-1", "value"),
    prevent_initial_call=True,
)
def set_freq_1_by_num(value):
    return [freq_list[int(value)], 250] if value not in [None, "", 0] else ["", ""]


@app.callback(
    Output("freq-2", "value", allow_duplicate=True),
    Output("time-2", "value", allow_duplicate=True),
    Input("freq-select-2", "value"),
    prevent_initial_call=True,
)
def set_freq_2_by_num(value):
    return [freq_list[int(value)], 250] if value not in [None, "", 0] else ["", ""]


@app.callback(
    Output("freq-1", "value"),
    Output("freq-2", "value"),
    Output("freq-select-1", "value"),
    Output("freq-select-2", "value"),
    Output("time-1", "value"),
    Output("time-2", "value"),
    Input("freq-clear", "n_clicks"),
    prevent_initial_call=True,
)
def clear_values(n_clicks):
    return [None] * 6


@app.callback(
    Output("play-results", "children"),
    Input("freq-play", "n_clicks"),
    State("freq-1", "value"),
    State("freq-2", "value"),
    State("time-1", "value"),
    State("time-2", "value"),
    prevent_initial_call=True,
)
def play_sound(n_clicks, freq_1, freq_2, time_1, time_2):
    time_1 = time_1 / 1000
    time_2 = time_2 / 1000

    freq_lst = [[freq_1, time_1], [freq_2, time_2]]

    # play_tone(freq_lst)
    threading.Thread(target=play_tone_versh, args=([freq_lst])).start()

    return dmc.Group(
        [
            "Воспроизведено",
            dcc.Markdown(f"$f_1 = {freq_1}\\, Гц$", mathjax=True),
            "и",
            dcc.Markdown(f"$f_2 = {freq_2}\\, Гц$", mathjax=True),
        ]
    )


# def open_browser():
#     if not os.environ.get("WERKZEUG_RUN_MAIN"):
#         webbrowser.open_new("http://localhost:{}".format(81))


dev = True

if __name__ == "__main__":
    # Timer(1, open_browser).start()
    if dev:
        app.run(debug=True, host="0.0.0.0", port=81)
    else:
        from waitress import serve

        serve(app.server, host="0.0.0.0", port=81)
