import os
import json
from itertools import cycle
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QSizePolicy,
    QDesktopWidget,
    QApplication,
)
from PyQt5.QtCore import Qt
from gui_talkbot_decorator import Decorator
from gui_talkbot_css import CssForMainWindow
from gui_talkbot_widget_label import (
    QLabelBot,
    QLabelYou,
)
from gui_talkbot_widget_page import (
    QPage00,
    QPage01,
)


class MainWindowBase(QMainWindow):
    msg_bot_ng = 'ただいま準備中です ...\n少々お待ちくださいませ ...'
    msg_bot_ok = 'お待たせいたしました！\nさっそくお話しましょう！'
    msg_exit = '退出する'
    msgs_help = [  # It is impossible to align columns if the font is not "Monotype".
        ' 一番下の欄に文字を入力します',
        ' ↑↓  : ボットタイプ変更',
        '   F1  : 画面の切替（メイン画面 <--> 操作説明画面）',
        '   F11 : 入力メッセージをクリア',
        '   F12 : ウィンドウサイズをデフォルトに戻す',
        '   Esc : アプリ終了',
    ]

    decorator = Decorator()

    @decorator.elapse_time_measurement
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_config_from_json()
        self.setup_bot_info()
        self.make_widgets()
        self.setup_widgets()
        self.setup_layouts()
        self.setup_style_sheets()
        self.setup_main_window()
        self.setup_sound_effects()
        self.setup_timers_and_workers()
        self.setup_threads_and_workers()
        self.setup_signal_connections()
        self.setup_signal_connections_for_user_actions()
        self.setup_focus()

    def load_config_from_json(self):
        desktop = QDesktopWidget()
        size_desktop = desktop.screenGeometry()
        size_frame = self.frameSize()
        self.window_x_default = int(size_desktop.width() / 2 - size_frame.width() / 2)
        self.window_y_default = int(size_desktop.height() / 2 - size_frame.height() / 2)

        self.window_x = self.window_x_default
        self.window_y = self.window_y_default
        self.window_w = self.config.WINDOW_W_MIN
        self.window_h = self.config.WINDOW_H_MIN
        self.type_bot = self.config.TYPE_BOT
        vars_config = (
            ('WINDOW_X', 'window_x'),
            ('WINDOW_Y', 'window_y'),
            ('WINDOW_W', 'window_w'),
            ('WINDOW_H', 'window_h'),
            ('TYPE_BOT', 'type_bot'),
        )

        if not os.path.exists(self.config.PATH_JSON):
            return

        with open(self.config.PATH_JSON, mode='r', encoding='utf-8') as file:
            config_from_json = json.load(file)

        for data in vars_config:
            key = data[0]
            name = data[1]
            value = getattr(self, name)
            try:
                value = config_from_json[key]
            except KeyError:
                pass
            setattr(self, name, value)

    def setup_bot_info(self):
        self.types_bot = cycle(self.config.TYPES_BOT.keys())
        try:
            self.name_bot = self.config.TYPES_BOT[self.type_bot]
        except KeyError:
            self.type_bot = 0
            self.name_bot = self.config.TYPES_BOT[self.type_bot]

    def make_widgets(self):
        self.central = QStackedWidget()

        self.pages = [
            {"Page": QPage00(), "Filter": QWidget(), "Layout": QVBoxLayout()},
            {"Page": QPage01(), "Filter": QWidget(), "Layout": QVBoxLayout()},
        ]

        self.label_bot = QLabelBot()
        self.label_you = QLabelYou()

        num = len(self.config.TYPES_BOT)
        self.buttons_bot_type = [QPushButton() for i in range(num)]
        self.button_exit = QPushButton()
        self.button_help = QPushButton()
        self.inputbox = QLineEdit()

        num = len(self.msgs_help)
        self.labels_help = [QLabel() for i in range(num)]
        self.button_back = QPushButton()

    def setup_widgets(self):
        self.pages[0]["Page"].setObjectName(self.config.WIDGET_NAME_PAGE_00)
        self.pages[1]["Page"].setObjectName(self.config.WIDGET_NAME_PAGE_01)
        self.pages[0]["Filter"].setObjectName(self.config.WIDGET_NAME_PAGE_BG_FILTER)
        self.pages[1]["Filter"].setObjectName(self.config.WIDGET_NAME_PAGE_BG_FILTER)

        self.label_bot.setTextWithInterval(self.msg_bot_ng)
        self.label_you.setTextWithInterval(' ')
        self.label_bot.setAlignment(Qt.AlignLeft)
        self.label_you.setAlignment(Qt.AlignLeft)
        self.label_bot.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label_you.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label_bot.setWordWrap(True)
        self.label_you.setWordWrap(True)

        for idx, name in enumerate(self.config.TYPES_BOT.values()):
            self.buttons_bot_type[idx].setText(name)

        self.button_exit.setText(self.msg_exit)
        self.button_help.setText('?')
        self.inputbox.setText('')

        num = len(self.msgs_help)
        for i in range(num):
            self.labels_help[i].setText(self.msgs_help[i])
        self.button_back.setText('←')

    def setup_style_sheets(self):
        inst_css = CssForMainWindow()
        data_css = inst_css.get_all_css_data()
        self.data_css = data_css

        css = data_css["label_help"]
        for label in self.labels_help:
            label.setStyleSheet(css)

        self.label_bot.set_css(data_css["label_bot_ready_ng"])
        self.label_you.set_css(data_css["label_you"])
        self.button_exit.setStyleSheet(data_css["button_exit"])
        self.button_help.setStyleSheet(data_css["button_help"])
        self.button_back.setStyleSheet(data_css["button_help"])
        self.inputbox.setStyleSheet(data_css["input_user"])
        self.pages[0]["Page"].setStyleSheet(data_css["page_bg_img_00"])
        self.pages[1]["Page"].setStyleSheet(data_css["page_bg_img_01"])
        self.pages[0]["Filter"].setStyleSheet(data_css["page_bg_filter"])
        self.pages[1]["Filter"].setStyleSheet(data_css["page_bg_filter"])

        self.update_css_for_bot_type_buttons()

    def update_css_for_bot_type_buttons(self):
        buttons = self.buttons_bot_type
        num_buttons = len(self.buttons_bot_type)
        css_a = self.data_css["button_bot"]
        css_c = self.data_css["button_bot_crr"]
        idx_a = -1
        idx_c = self.type_bot
        for idx_a in range(num_buttons):
            if idx_a != idx_c:
                buttons[idx_a].setStyleSheet(css_a)
            else:
                buttons[idx_c].setStyleSheet(css_c)

    def setup_layouts(self):
        self.setup_layouts_page_00()
        self.setup_layouts_page_01()
        self.setup_layouts_page_99()

    def setup_layouts_page_00(self):
        layout_v = QVBoxLayout()
        layout_bot_type = QHBoxLayout()
        layout_talk = QHBoxLayout()
        layout_under = QHBoxLayout()

        addWidget = layout_bot_type.addWidget
        for button in self.buttons_bot_type:
            addWidget(button)

        layout_talk.addWidget(self.label_bot)
        layout_talk.addWidget(self.label_you)

        layout_under.addWidget(self.inputbox)
        layout_under.addWidget(self.button_help)

        layout_v.addWidget(self.button_exit)
        layout_v.addLayout(layout_bot_type)
        layout_v.addLayout(layout_talk)
        layout_v.addLayout(layout_under)

        self.pages[0]["Filter"].setLayout(layout_v)

    def setup_layouts_page_01(self):
        layout_v = QVBoxLayout()

        for label in self.labels_help:
            layout_v.addWidget(label)
        layout_v.addWidget(self.button_back, alignment=Qt.AlignRight)

        self.pages[1]["Filter"].setLayout(layout_v)

    def setup_layouts_page_99(self):
        for layers in self.pages:
            layers["Layout"].setContentsMargins(0, 0, 0, 0)
            layers["Layout"].setSpacing(0)
            layers["Layout"].addWidget(layers["Filter"])
            layers["Page"].setLayout(layers["Layout"])
            self.central.addWidget(layers["Page"])
        page = self.pages[0]["Page"]
        self.central.setCurrentWidget(page)
        self.setCentralWidget(self.central)

    def setup_main_window(self):
        self.setWindowTitle(self.config.WINDOW_TITLE)
        self.setMinimumSize(self.config.WINDOW_W_MIN, self.config.WINDOW_H_MIN)
        self.resize(self.window_w, self.window_h)
        self.move(self.window_x, self.window_y)
        self.show()

    def setup_timers_and_workers(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def setup_threads_and_workers(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def setup_signal_connections(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def setup_signal_connections_for_user_actions(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def setup_sound_effects(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def setup_focus(self):
        self.inputbox.setFocusPolicy(Qt.StrongFocus)
        self.inputbox.setFocus()


if __name__ == '__main__':
    from common import attach_common

    @attach_common
    class MainWindowPage00Debug(MainWindowBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            page = self.pages[0]["Page"]
            self.central.setCurrentWidget(page)

    @attach_common
    class MainWindowPage01Debug(MainWindowBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            page = self.pages[1]["Page"]
            self.central.setCurrentWidget(page)

    TestClasses = (
        MainWindowPage00Debug,
        MainWindowPage01Debug,
    )

    import sys
    qapp = QApplication(sys.argv)
    for TestClass in TestClasses:
        window = TestClass()
        window.show()
        code = qapp.exec()
    sys.exit(code)
