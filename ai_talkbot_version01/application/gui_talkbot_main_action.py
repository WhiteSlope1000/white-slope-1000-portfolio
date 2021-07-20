from PyQt5.QtGui import (
    QKeySequence,
)
from PyQt5.QtWidgets import (
    QMainWindow,
)


class MainWindowGuiUserAction(QMainWindow):
    page_idx = 0

    def setup_signal_connections_for_user_actions(self):
        self.buttons_bot_type[0].clicked.connect(self.play_mouse_click_sound)
        self.buttons_bot_type[1].clicked.connect(self.play_mouse_click_sound)
        self.buttons_bot_type[2].clicked.connect(self.play_mouse_click_sound)
        self.buttons_bot_type[3].clicked.connect(self.play_mouse_click_sound)
        self.button_exit.clicked.connect(self.play_mouse_click_sound)
        self.button_help.clicked.connect(self.play_mouse_click_sound)
        self.button_back.clicked.connect(self.play_mouse_click_sound)
        self.inputbox.returnPressed.connect(self.play_key_press_sound)

        self.buttons_bot_type[0].clicked.connect(self.change_bot_type_to_0)
        self.buttons_bot_type[1].clicked.connect(self.change_bot_type_to_1)
        self.buttons_bot_type[2].clicked.connect(self.change_bot_type_to_2)
        self.buttons_bot_type[3].clicked.connect(self.change_bot_type_to_3)
        self.button_exit.clicked.connect(self.close_app)
        self.button_help.clicked.connect(self.switch_page_from_button_help)
        self.button_back.clicked.connect(self.switch_page_from_button_back)
        self.inputbox.returnPressed.connect(self.show_msg)


class MainWindowKeybind(QMainWindow):
    def keyPressEvent(self, evt):
        keycode_key = evt.key()

        token_key = QKeySequence(keycode_key).toString()
        try:
            token_key.encode('utf-8')
        except UnicodeEncodeError:
            token_key = 'UnicodeEncodeError'

        msg = f'current page, pressed key: {self.page_idx} "{token_key}"'
        self.logger.i(msg)

        if token_key == '':
            pass
        elif token_key == 'F1':
            self.play_key_press_sound()
            self.page_idx = 1 if self.page_idx == 0 else 0
            self.switch_page_widget(self.page_idx)
        elif token_key == 'F11':
            self.play_key_press_sound()
            self.clear_inputbox()
        elif token_key == 'F12':
            self.play_key_press_sound()
            self.initialize_window_size()
        elif token_key == 'Up':
            if self.page_idx != 0:
                return
            self.play_key_press_sound()
            type_bot = self.type_bot + 1
            self.change_bot(type_bot)
        elif token_key == 'Down':
            if self.page_idx != 0:
                return
            self.play_key_press_sound()
            type_bot = self.type_bot - 1
            self.change_bot(type_bot)
        elif token_key == 'Esc':
            if self.page_idx != 0:
                return
            self.play_key_press_sound()
            self.close_app()


if __name__ == '__main__':
    from gui_talkbot import MainWindow
    TestClass = MainWindow

    import sys
    from PyQt5.QtWidgets import QApplication
    qapp = QApplication(sys.argv)
    window = TestClass()
    window.show()
    code = qapp.exec()
    sys.exit(code)
