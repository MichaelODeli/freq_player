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
    "Частота модуляции": 1600,
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
                                label="Установка времени",
                                opened=True,
                                leftSection=get_icon(icon="material-symbols:call"),
                                children=[
                                    dmc.NavLink(
                                        label="Установить t = 1 c",
                                        description="Для вызова радиостанции и/или телефона",
                                        id="freq-phone-set_time-1sec",
                                        leftSection=get_icon(
                                            icon="mdi:clock-time-two-outline"
                                        ),
                                        style={"line-height": "1.3"},
                                    ),
                                    dmc.NavLink(
                                        label="Установить t = 0.25 c",
                                        description="Для отмены или контоля вызова",
                                        id="freq-phone-set_time-025sec",
                                        leftSection=get_icon(
                                            icon="mdi:clock-time-two-outline"
                                        ),
                                        style={"line-height": "1.3"},
                                    ),
                                ],
                            ),
                            dmc.NavLink(
                                label="Установка частот",
                                opened=True,
                                leftSection=get_icon(icon="carbon:radio"),
                                children=[
                                    dmc.NavLink(
                                        label="Вызов радиостанции",
                                        description="Устанавливается первая частота из трехчастотной посылки - частота модуляции. "
                                        "Остальные частоты соответствуют номеру СИП радиостанции.",
                                        id="freq-set_freq-call_rs",
                                        leftSection=get_icon(
                                            icon="material-symbols:call"
                                        ),
                                    ),
                                ],
                            ),
                            dmc.NavLink(
                                label="Специальные команды",
                                opened=True,
                                leftSection=get_icon(icon="carbon:radio"),
                                children=[
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
                                    dmc.AccordionPanel("some text"),
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
                                                dmc.Alert(
                                                    "Вы ввели неверные частоты и/или неверные длительности сигналов. Попробуйте еще раз.",
                                                    title="Ошибка ввода частот",
                                                    hide=True,
                                                    id="freq-alert",
                                                    color="red",
                                                    duration=3000,
                                                ),
                                                fields.render_freq_1_fields(FREQ_LIST),
                                                fields.render_freq_2_fields(FREQ_LIST),
                                                fields.render_freq_3_fields(FREQ_LIST),
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
                ),
            ],
            navbar={
                "width": 350,
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
    Output("play-results", "children", allow_duplicate=True),
    Output("freq-select-1", "value", allow_duplicate=True),
    Output("freq-select-2", "value", allow_duplicate=True),
    Output("freq-select-3", "value", allow_duplicate=True),
    Output("time-1", "value", allow_duplicate=True),
    Output("time-2", "value", allow_duplicate=True),
    Output("time-3", "value", allow_duplicate=True),
    Input("freq-phone-set_time-1sec", "n_clicks"),
    Input("freq-phone-set_time-025sec", "n_clicks"),
    Input("freq-set_freq-call_rs", "n_clicks"),
    Input("freq-cancel", "n_clicks"),
    Input("freq-control", "n_clicks"),
    Input("freq-clear", "n_clicks"),
    prevent_initial_call=True,
)
def set_specify_freq(n0, n1, n2, n3, n4, n5):
    func_name = ctx.triggered_id

    # special functions
    if func_name == "freq-phone-set_time-1sec":
        return [no_update] + [no_update] * 3 + [PHONE_PLAY_TIME] * 3
    elif func_name == "freq-phone-set_time-025sec":
        return [no_update] + [no_update] * 3 + [CANCEL_CONTROL_TIME] * 3
    elif func_name == "freq-set_freq-call_rs":
        return (
            [no_update]
            + ["Частота модуляции"]
            + [no_update] * 2
            + [PHONE_PLAY_TIME] * 3
        )
    elif func_name == "freq-cancel":
        return (
            [no_update]
            + ["2", "6", None]
            + [CANCEL_CONTROL_TIME, CANCEL_CONTROL_TIME, ""]
        )
    elif func_name == "freq-control":
        return (
            [no_update]
            + ["6", "2", None]
            + [CANCEL_CONTROL_TIME, CANCEL_CONTROL_TIME, ""]
        )
    else:
        return [None]*4 + [""]*3


@app.callback(
    Output("freq-1", "value", allow_duplicate=True),
    Input("freq-select-1", "value"),
    prevent_initial_call=True,
)
def set_freq_1_by_num(value):
    try:
        value = int(value)
    except Exception:
        pass
    return FREQ_LIST[value] if value not in [None, "", 0] else ""


@app.callback(
    Output("freq-2", "value", allow_duplicate=True),
    Input("freq-select-2", "value"),
    prevent_initial_call=True,
)
def set_freq_2_by_num(value):
    try:
        value = int(value)
    except Exception:
        pass
    return FREQ_LIST[value] if value not in [None, "", 0] else ""


@app.callback(
    Output("freq-3", "value", allow_duplicate=True),
    Input("freq-select-3", "value"),
    prevent_initial_call=True,
)
def set_freq_3_by_num(value):
    try:
        value = int(value)
    except Exception:
        pass
    return FREQ_LIST[value] if value not in [None, "", 0] else ""


@app.callback(
    Output("play-results", "children"),
    Output("freq-alert", "hide"),
    Input("freq-play", "n_clicks"),
    State("freq-1", "value"),
    State("freq-2", "value"),
    State("freq-3", "value"),
    State("time-1", "value"),
    State("time-2", "value"),
    State("time-3", "value"),
    prevent_initial_call=True,
    running=[(Output("freq-play", "disabled"), True, False)],
)
def play_sound(n_clicks, freq_1, freq_2, freq_3, time_1, time_2, time_3):
    if (
        None in [freq_1, freq_2, time_1, time_2]
        or "" in [freq_1, freq_2, time_1, time_2]
        or (freq_3 not in [None, ""] and time_3 in [None, ""])
        or freq_1 > 8000
        or freq_2 > 8000
        or time_1 > 60000
        or time_2 > 60000
    ):
        return (None, False)
    elif freq_3 not in [None, ""]:
        if freq_3 < 8000 and time_3 < 60000:
            freq_lst, full_wave = freq_player.play_3(
                freq_1,
                freq_2,
                freq_3,
                int(time_1),
                int(time_2),
                int(time_3),
                return_vals=True,
            )
            sleep(int(time_1) / 1000 + int(time_2) / 1000 + int(time_3) / 1000)
        else:
            return (None, False)
    else:
        freq_lst, full_wave = freq_player.play_2(
            freq_1, freq_2, int(time_1), int(time_2), return_vals=True
        )
        sleep(int(time_1) / 1000 + int(time_2) / 1000)
    fig = freq_drawer.get_fig(freq_lst, full_wave)

    return dcc.Graph(figure=fig), True


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
