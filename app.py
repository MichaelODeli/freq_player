import threading

import dash
import dash_mantine_components as dmc
import flask
import plotly.graph_objects as go
from dash import Input, Output, State, ctx, dcc, html, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import freq_drawer
import freq_maker
import styles

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

FREQ_LIST = {
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

PHONE_PLAY_TIME = 1000
CANCEL_CONTROL_TIME = 250
LISTEN_SEND_TIME = 100


def play(freq_1, freq_2, time_1, time_2):
    freq_lst = [[freq_1, time_1 / 1000], [freq_2, time_2 / 1000]]
    full_wave = freq_maker.generate_tone(freq_lst)
    threading.Thread(target=freq_maker.play_tone, args=([full_wave])).start()


# Конструкция всего макета
app.layout = dmc.MantineProvider(
    children=[
        dcc.Store(id="freq-play-mode"),
        dmc.AppShell(
            [
                dmc.AppShellNavbar(
                    children=html.Div(
                        [
                            dmc.NavLink(
                                label="Основные операции",
                                opened=True,
                                children=[
                                    dmc.NavLink(
                                        label="Очистить",
                                        id="freq-clear",
                                        leftSection=get_icon(icon="mdi:clear"),
                                    ),
                                ],
                            ),
                            dmc.NavLink(
                                label="Работа с телефоном",
                                opened=True,
                                children=[
                                    dmc.NavLink(
                                        label="Настроить время",
                                        description="Время подачи - 1 с",
                                        id="freq-phone-set_time",
                                        leftSection=get_icon(
                                            icon="mdi:clock-time-two-outline"
                                        ),
                                    ),
                                ],
                            ),
                            dmc.NavLink(
                                label="Работа с РС-46МЦ",
                                opened=True,
                                children=[
                                    dmc.NavLink(
                                        label='Режим "Прием"',
                                        description="Отпустить тангенту",
                                        id="freq-rx",
                                        leftSection=get_icon(
                                            icon="material-symbols:call-received"
                                        ),
                                    ),
                                    dmc.NavLink(
                                        label='Режим "Передача"',
                                        description="Нажать тангенту",
                                        id="freq-tx",
                                        leftSection=get_icon(
                                            icon="material-symbols:call-made"
                                        ),
                                    ),
                                    # dmc.NavLink(
                                    #     label='Режим разговора',
                                    #     id="freq-speak-mode",
                                    #     leftSection=get_icon(
                                    #         icon="material-symbols:call-made"
                                    #     ),
                                    # ),
                                    # dmc.NavLink(
                                    #     label='Вызов "ЛОК"',
                                    #     id="freq-call-loc",
                                    #     leftSection=get_icon(
                                    #         icon="solar:call-cancel-outline"
                                    #     ),
                                    #     disabled=True,
                                    # ),
                                    dmc.NavLink(
                                        label="Отбой",
                                        id="freq-cancel",
                                        leftSection=get_icon(
                                            icon="solar:call-cancel-outline"
                                        ),
                                    ),
                                    dmc.NavLink(
                                        label="Контроль",
                                        id="freq-control",
                                        leftSection=get_icon(
                                            icon="mdi:user-access-control"
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                dmc.AppShellMain(
                    dmc.Stack(
                        [
                            dmc.Stack(
                                [
                                    dmc.Group(
                                        [
                                            dmc.Select(
                                                label="Номер частоты 1",
                                                data=[str(i) for i in FREQ_LIST.keys()],
                                                w=150,
                                                id="freq-select-1",
                                                clearable=True,
                                            ),
                                            dmc.NumberInput(
                                                label="Частота 1, Гц", id="freq-1"
                                            ),
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
                                                data=[str(i) for i in FREQ_LIST.keys()],
                                                w=150,
                                                id="freq-select-2",
                                                clearable=True,
                                            ),
                                            dmc.NumberInput(
                                                label="Частота 2, Гц", id="freq-2"
                                            ),
                                            dmc.NumberInput(
                                                label="Время подачи, мс", id="time-2"
                                            ),
                                        ]
                                    ),
                                    dmc.Switch(
                                        size="md",
                                        radius="lg",
                                        label="Автовоспроизведение",
                                        checked=False,
                                        id="freq-autoplay",
                                    ),
                                    dmc.Button(
                                        "Воспроизвести", id="freq-play", fullWidth=True
                                    ),
                                    dmc.Group(id="freq-speak-modes"),
                                ],
                                px="sm",
                                pt="sm",
                                w="max-content",
                                gap="lg",
                            ),
                            html.Div(id="play-results", style={"width": "1500px"}),
                        ]
                    )
                ),
            ],
            navbar={
                "width": 250,
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
    Output("time-1", "value", allow_duplicate=True),
    Output("time-2", "value", allow_duplicate=True),
    Output("play-results", "children", allow_duplicate=True),
    Input("freq-clear", "n_clicks"),
    Input("freq-phone-set_time", "n_clicks"),
    Input("freq-cancel", "n_clicks"),
    Input("freq-control", "n_clicks"),
    Input("freq-rx", "n_clicks"),
    Input("freq-tx", "n_clicks"),
    State("freq-autoplay", "checked"),
    prevent_initial_call=True,
)
def set_specify_freq(n0, n1, n2, n3, n4, n5, autoplay):
    func_name = ctx.triggered_id

    # special functions
    if func_name == "freq-phone-set_time":
        return [no_update] * 2 + [str(PHONE_PLAY_TIME)] * 2 + [no_update]
    if func_name == "freq-clear":
        return [None] * 2 + [""] * 2 + [None]

    # set specify freq
    if func_name == "freq-cancel":
        freq_ids = [2, 6]
        play_time = CANCEL_CONTROL_TIME
    elif func_name == "freq-control":
        freq_ids = [6, 2]
        play_time = CANCEL_CONTROL_TIME
    elif func_name == "freq-rx":
        freq_ids = [38, 36]
        play_time = LISTEN_SEND_TIME
    elif func_name == "freq-tx":
        freq_ids = [36, 38]
        play_time = LISTEN_SEND_TIME
    else:
        raise PreventUpdate

    if autoplay:
        play(FREQ_LIST[freq_ids[0]], FREQ_LIST[freq_ids[1]], play_time, play_time)

    return [str(fr) for fr in freq_ids] + [str(play_time)] * 2 + [no_update]


@app.callback(
    Output("freq-1", "value", allow_duplicate=True),
    Input("freq-select-1", "value"),
    prevent_initial_call=True,
)
def set_freq_1_by_num(value):
    return FREQ_LIST[int(value)] if value not in [None, "", 0] else ""


@app.callback(
    Output("freq-2", "value", allow_duplicate=True),
    Input("freq-select-2", "value"),
    prevent_initial_call=True,
)
def set_freq_2_by_num(value):
    return FREQ_LIST[int(value)] if value not in [None, "", 0] else ""


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
    freq_lst = [[freq_1, int(time_1) / 1000], [freq_2, int(time_2) / 1000]]
    full_wave = freq_maker.generate_tone(freq_lst)
    threading.Thread(target=freq_maker.play_tone, args=([full_wave])).start()

    fig = freq_drawer.get_fig(freq_lst, full_wave)

    return dcc.Graph(figure=fig)


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
