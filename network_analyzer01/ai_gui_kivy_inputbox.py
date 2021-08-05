import time
from ai_gui_kivy_config import (
    ConfigAddon,
    Config,
)
from kivy.core.window import (
    core_select_lib,
    window_impl,
    Window,
)
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import (
    LabelBase,
    DEFAULT_FONT,
)
from kivy.uix.label import Label
from kivy.graphics import (
    Color,
    Rectangle,
)
from kivy.cache import Cache
from kivy.base import EventLoop
from kivy.resources import resource_add_path
from core_logger import Logging
logger = Logging(__name__).get_logger()


resource_add_path('c:/Windows/Fonts')
LabelBase.register(DEFAULT_FONT, 'msgothic.ttc')


class InputboxCustom(TextInput):
    config_addon = ConfigAddon()
    root = None
    interval_enter_old = 0.0  # sec

    def set_root(self, root):
        self.root = root
        self.args = self.root.args

    def on_text_validate(self, *args):
        msg = 'enter is pressed'
        logger.i(msg)

        time_crr = time.time()
        time_dif = time_crr - self.interval_enter_old
        self.interval_enter_old = time_crr

        msg = f'interval: {time_dif:2.2f}'
        logger.i(msg)

        if time_dif > self.config_addon.INTERVAL_ENTER:
            return

        msg = 'enter is pressed twice quickly'
        logger.i(msg)

        # path = self.args[0]
        # with open(path, mode='w', encoding='utf-8') as file:
        #     file.write(self.text)
        #     logger.i(self.text)

        self.root.text_filter = self.text
        self.root.root_window.close()


class LabelBgColor(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 0.5)
            Rectangle(
                pos=self.pos,
                size=self.size,
            )
            Color(0.3, 0.3, 0.3, 0.5)
            Rectangle(
                pos=(self.pos[0] + 1, self.pos[1] + 0),
                size=(self.size[0] - 2, self.size[1] - 1),
            )


class Inputbox(App):
    config_addon = ConfigAddon()
    args = []
    text_filter = ''

    def get_filter_text(self):
        return self.text_filter

    def build(self):
        # path = self.args[0]
        # try:
        #     with open(path, mode='r', encoding='utf-8') as file:
        #         text = file.readline()
        #         logger.i(text)
        # except FileNotFoundError:
        #     with open(path, mode='w', encoding='utf-8') as file:
        #         text = ''
        #         logger.i(text)

        Window.bind(on_key_down=self.on_key_down)
        self.text_filter = self.args[-1]

        self.inputbox = InputboxCustom()
        self.inputbox.text = self.text_filter
        self.inputbox.multiline = False
        self.inputbox.text_validate_unfocus = False
        self.inputbox.focus = True
        self.inputbox.background_color = self.config_addon.BG_COLOR
        self.inputbox.cursor_width = self.config_addon.CURSOR_WIDTH
        self.inputbox.cursor_color = self.config_addon.CURSOR_COLOR
        self.inputbox.font_size = self.config_addon.FONT_SIZE
        self.inputbox.set_root(self)

        self.label = LabelBgColor()
        self.label.text = 'Press "Enter" twice quickly for [Enter]. Press "Esc" for [Cancel].'
        self.label.focus = False
        self.label.color = (1.0, 1.0, 0.5, 0.8)
        self.label.outline_width = 1
        self.label.outline_color = (0.3, 0.3, 0.3)
        self.label.font_size = self.config_addon.FONT_SIZE

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.inputbox)
        return self.layout

    def on_key_down(self, keyboard, *args):
        msg = f'key event: {list(args)}'
        logger.i(msg)
        keycode = args[0]
        if keycode == 27:
            self.root_window.close()


class Reset(object):
    def __init__(self):
        global Window
        Config  # just for suppressing pep8 warning ...
        if not EventLoop.event_listeners:
            Window = core_select_lib(
                'window',
                window_impl,
                True,
            )
            # Cache.print_usage()
            for category in Cache._categories:
                Cache._objects[category] = {}


if __name__ == '__main__':
    Reset()
    args = [
        'meros_b.log',
        '私',
    ]
    app = Inputbox()
    app.args = args
    app.run()
    msg = app.get_filter_text()
    logger.i(msg)
