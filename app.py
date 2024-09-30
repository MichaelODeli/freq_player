import os
import webbrowser
from time import sleep

import dash
import dash_mantine_components as dmc
import flask
from dash import Input, Output, State, ctx, dcc, html, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import views.styles as styles
from controllers import freq_drawer, freq_player
from views import fields

dash._dash_renderer._set_react_version("18.2.0")


def get_icon(icon):
    return DashIconify(icon=icon, height=20)


# flask and dash configuration
server = flask.Flask("PlaySound")
app = dash.Dash(
    "PlaySound",
    server=server,
    external_stylesheets=styles.STYLESHEETS,
    title="PlaySound",
    update_title="PlaySound 🔃",
    suppress_callback_exceptions=True,
)

FREQ_LIST = {
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
                                label="Работа с телефоном",
                                opened=True,
                                leftSection=get_icon(icon="material-symbols:call"),
                                children=[
                                    dmc.NavLink(
                                        label="Настроить время подачи сигнала",
                                        description="t = 1 с",
                                        id="freq-phone-set_time",
                                        leftSection=get_icon(
                                            icon="mdi:clock-time-two-outline"
                                        ),
                                        style={"line-height": "1.3"},
                                    ),
                                ],
                            ),
                            dmc.NavLink(
                                label="Работа с РС-46МЦ",
                                opened=True,
                                leftSection=get_icon(icon="carbon:radio"),
                                children=[
                                    dmc.NavLink(
                                        label="Режим разговора",
                                        id="freq-speak-mode",
                                        leftSection=get_icon(
                                            icon="material-symbols:call"
                                        ),
                                        description='Проверьте, что включен пункт "Автоматическое воспроизведение"',
                                    ),
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
                                        description="Отмена текущего вызова",
                                    ),
                                    dmc.NavLink(
                                        label="Контроль",
                                        id="freq-control",
                                        leftSection=get_icon(
                                            icon="mdi:user-access-control"
                                        ),
                                        description="Проверка соединения",
                                    ),
                                ],
                            ),
                            dmc.NavLink(
                                label="Очистить данные",
                                id="freq-clear",
                                leftSection=get_icon(icon="ant-design:clear-outlined"),
                                description="Очистка всех полей ввода",
                            ),
                        ],
                    ),
                ),
                dmc.AppShellMain(
                    dmc.Accordion(
                        multiple=True,
                        value=[
                            "data_input",
                        ],
                        children=[
                            dmc.AccordionItem(
                                [
                                    dmc.AccordionControl(
                                        "Информация по подключению",
                                        icon=get_icon("material-symbols:help-outline"),
                                    ),
                                    dmc.AccordionPanel("Для подачи сигнала, используйте номера СИП. По умолчанию СИП1 = 1, тогда частоты будут 2 и 7."
                                                       "Фиолетовый - TIP, синий - SLEEVE"),
                                ],
                                value="help",
                            ),
                            dmc.AccordionItem(
                                [
                                    dmc.AccordionControl(
                                        "Ввод данных", icon=get_icon("ri:input-field")
                                    ),
                                    dmc.AccordionPanel(
                                        dmc.Stack(
                                            [
                                                fields.render_freq_1_fields(FREQ_LIST),
                                                fields.render_freq_2_fields(FREQ_LIST),
                                            ]
                                            + fields.render_freq_buttons(),
                                            px="sm",
                                            pt="sm",
                                            w="max-content",
                                            gap="lg",
                                        ),
                                    ),
                                ],
                                value="data_input",
                            ),
                            dmc.AccordionItem(
                                [
                                    dmc.AccordionControl(
                                        "График сигнала",
                                        icon=get_icon(
                                            "streamline:interface-signal-graph-heart-line-beat-square-graph-stats"
                                        ),
                                    ),
                                    dmc.AccordionPanel(
                                        html.Div(
                                            id="play-results",
                                            style={"width": "1500px"},
                                            children=[
                                                'График отобразится после нажатия кнопки "Воспроизвести"'
                                            ],
                                        )
                                    ),
                                ],
                                value="graph",
                            ),
                        ],
                    ),
                    # dmc.Stack(
                    #     [
                    #         dmc.Stack(
                    #             [
                    #                 dmc.Group(
                    #                     [
                    #                         dmc.Select(
                    #                             label="Номер частоты 1",
                    #                             data=[str(i) for i in FREQ_LIST.keys()],
                    #                             w=150,
                    #                             id="freq-select-1",
                    #                             clearable=True,
                    #                         ),
                    #                         dmc.NumberInput(
                    #                             label="Частота 1, Гц", id="freq-1"
                    #                         ),
                    #                         dmc.NumberInput(
                    #                             label="Время подачи, мс",
                    #                             id="time-1",
                    #                         ),
                    #                     ]
                    #                 ),
                    #                 dmc.Group(
                    #                     [
                    #                         dmc.Select(
                    #                             label="Номер частоты 2",
                    #                             data=[str(i) for i in FREQ_LIST.keys()],
                    #                             w=150,
                    #                             id="freq-select-2",
                    #                             clearable=True,
                    #                         ),
                    #                         dmc.NumberInput(
                    #                             label="Частота 2, Гц", id="freq-2"
                    #                         ),
                    #                         dmc.NumberInput(
                    #                             label="Время подачи, мс", id="time-2"
                    #                         ),
                    #                     ]
                    #                 ),
                    #                 dmc.Switch(
                    #                     size="md",
                    #                     radius="lg",
                    #                     label="Автовоспроизведение",
                    #                     checked=True,
                    #                     id="freq-autoplay",
                    #                 ),
                    #                 dmc.Button(
                    #                     "Воспроизвести", id="freq-play", fullWidth=True
                    #                 ),
                    #                 dmc.Group(
                    #                     id="freq-speak-modes",
                    #                     children=[
                    #                         dmc.Button(
                    #                             "Нажать тангенту", id="freq-tx", w="40%"
                    #                         ),
                    #                         dmc.Button(
                    #                             "Отпустить тангенту",
                    #                             id="freq-rx",
                    #                             w="40%",
                    #                         ),
                    #                     ],
                    #                     display="none",
                    #                     justify="space-between",
                    #                 ),
                    #             ],
                    #             px="sm",
                    #             pt="sm",
                    #             w="max-content",
                    #             gap="lg",
                    #         ),
                    #         html.Div(id="play-results", style={"width": "1500px"}),
                    #     ]
                    # ),
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
    Output("freq-speak-modes", "display"),
    Output("freq-rx", "disabled"),
    Output("freq-tx", "disabled"),
    Output("freq-play", "disabled"),
    Input("freq-speak-mode", "n_clicks"),
    Input("freq-clear", "n_clicks"),
    Input("freq-phone-set_time", "n_clicks"),
    Input("freq-cancel", "n_clicks"),
    Input("freq-control", "n_clicks"),
    Input("freq-rx", "n_clicks"),
    Input("freq-tx", "n_clicks"),
    State("freq-autoplay", "checked"),
    prevent_initial_call=True,
)
def set_specify_freq(n0, n1, n2, n3, n4, n5, n6, autoplay):
    func_name = ctx.triggered_id
    speak_modes_display = "none"
    rx_button_disabled = False
    tx_button_disabled = False
    play_button_disabled = False

    # special functions
    if func_name == "freq-phone-set_time":
        return (
            [no_update] * 2
            + [str(PHONE_PLAY_TIME)] * 2
            + [
                no_update,
                speak_modes_display,
                rx_button_disabled,
                tx_button_disabled,
                play_button_disabled,
            ]
        )
    if func_name == "freq-clear":
        return (
            [None] * 2
            + [""] * 2
            + [
                None,
                speak_modes_display,
                rx_button_disabled,
                tx_button_disabled,
                play_button_disabled,
            ]
        )
    if func_name == "freq-speak-mode":
        speak_modes_display = None
        freq_player.play(
            1400, 0, 2000, 0
        )
        return (
            [None] * 2
            + [""] * 2
            + [
                None,
                speak_modes_display,
                not rx_button_disabled,
                tx_button_disabled,
                not play_button_disabled,
            ]
        )
    else:
        # set specify freq
        if func_name == "freq-cancel":
            freq_ids = [2, 6]
            play_time = CANCEL_CONTROL_TIME
        elif func_name == "freq-control":
            freq_ids = [6, 2]
            play_time = CANCEL_CONTROL_TIME
        elif func_name == "freq-rx":
            rx_button_disabled = not rx_button_disabled
            play_button_disabled = not play_button_disabled
            speak_modes_display = None
            freq_ids = [38, 36]
            play_time = LISTEN_SEND_TIME
        elif func_name == "freq-tx":
            tx_button_disabled = not tx_button_disabled
            play_button_disabled = not play_button_disabled
            speak_modes_display = None
            freq_ids = [36, 38]
            play_time = LISTEN_SEND_TIME
        else:
            raise PreventUpdate

        if autoplay:
            freq_player.play(
                FREQ_LIST[freq_ids[0]], FREQ_LIST[freq_ids[1]], play_time, play_time
            )

        return (
            [str(fr) for fr in freq_ids]
            + [str(play_time)] * 2
            + [
                no_update,
                speak_modes_display,
                rx_button_disabled,
                tx_button_disabled,
                play_button_disabled,
            ]
        )


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
    State("freq-modulation-play", "checked"),
    prevent_initial_call=True,
    running=[(Output("freq-play", "disabled"), True, False)],
)
def play_sound(n_clicks, freq_1, freq_2, time_1, time_2, modulation_play):
    if modulation_play:
        freq_player.play(
            1600, 0, 1000, 0
        )

    freq_lst, full_wave = freq_player.play(
        freq_1, freq_2, int(time_1), int(time_2), return_vals=True
    )
    sleep(int(time_1) / 1000 + int(time_2) / 1000)
    fig = freq_drawer.get_fig(freq_lst, full_wave)

    return dcc.Graph(figure=fig)


def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new("http://localhost:{}".format(81))


dev = True

if __name__ == "__main__":
    # Timer(1, open_browser).start()
    if dev:
        app.run(debug=True, host="0.0.0.0", port=81)
    else:
        from waitress import serve

        serve(app.server, host="0.0.0.0", port=81)
        open_browser()
