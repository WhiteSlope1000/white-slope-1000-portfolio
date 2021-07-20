import json
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import (
    QMediaPlayer,
    QMediaContent,
)
from PyQt5.QtWidgets import (
    QMainWindow,
)
from PyQt5.QtCore import pyqtSignal as QSignal  # NOQA: F401
from PyQt5.QtCore import pyqtSlot as QSlot  # NOQA: F401
from gui_talkbot_decorator import Decorator
from gui_talkbot_timer import TalkBotTimer
from gui_talkbot_timer_worker import (
    TimerWorkerBase,
    TimerWorkerCloseApp,
)
from gui_talkbot_thread import TalkBotThread
from gui_talkbot_thread_worker import (
    ThreadWorkerBase,
)


class MainWindowFunc(QMainWindow):
    threads = {}
    timers = {}
    workers = {}

    msg_goodby = 'それでは ... さようなら！'
    msg_warning = '文字を入力してください。'

    bot = None
    lister = None
    play_media = []
    is_bot_ready = False
    is_app_close = False

    decorator = Decorator()

    def setup_sound_effects(self):
        self.setup_sound_of_button_clicked()

    def setup_sound_of_button_clicked(self):

        class Dummy(object):
            def stop(self):
                pass

            def play(self):
                pass

        dummy = Dummy()
        paths = [
            self.config.PATH_SE_START,
            self.config.PATH_SE_BUTTON,
            self.config.PATH_SE_KEY,
        ]
        for path in paths:
            sound = QMediaContent(QUrl.fromLocalFile(path))
            player = QMediaPlayer(self)
            player.setMedia(sound)
            if self.config.ENABLED_SE:
                self.play_media.append(player)
            else:
                self.play_media.append(dummy)
        self.play_media[0].play()

    def setup_timers_and_workers(self):
        self.setup_timers_and_workers_for_close_app()
        self.setup_timers_and_workers_for_show_msg()

    def setup_timers_and_workers_for_close_app(self):
        name = 'TimerWorkerCloseApp'

        worker = TimerWorkerCloseApp()
        worker.setObjectName(name)
        worker.daemon = True
        worker.parent = self

        timer = TalkBotTimer()
        timer.setObjectName(name)
        timer.setInterval(self.config.INTERVAL_APP_CLOSE)
        timer.timeout.connect(worker.run)
        timer.started.connect(worker.setup_worker)
        timer.stopped.connect(worker.clean_worker)

        self.workers[name] = worker
        self.timers[name] = timer

    def setup_timers_and_workers_for_show_msg(self):
        # ToDo: It might be possible to make timers on the main,
        # ToDo: and pass it to label instances.
        if 0:
            name = 'TimerWorkerBase'

            worker = TimerWorkerBase()
            worker.setObjectName(name)
            worker.daemon = True
            worker.parent = self

            timer = TalkBotTimer()
            timer.setObjectName(name)
            timer.setInterval(100)
            timer.started.connect(worker.setup_worker)
            timer.stopped.connect(worker.clean_worker)

            self.workers[name] = worker
            self.timers[name] = timer

    def setup_threads_and_workers(self):
        name = 'TalkBotThread'
        thread = TalkBotThread()
        thread.setObjectName(name)
        thread.daemon = True
        thread.parent = self

        # ToDo: Could be better to take a worker solution.
        if 0:
            worker = ThreadWorkerBase()
            worker.setObjectName(name)
            worker.daemon = True
            worker.parent = self

        self.threads[name] = thread
        self.threads[name].start()

    def setup_signal_connections(self):
        pass

    def change_bot_type_to_0(self):
        self.change_bot(0)

    def change_bot_type_to_1(self):
        self.change_bot(1)

    def change_bot_type_to_2(self):
        self.change_bot(2)

    def change_bot_type_to_3(self):
        self.change_bot(3)

    @decorator.bot_change_guard
    def change_bot(self, type_bot):
        min = 0
        max = len(self.config.TYPES_BOT) - 1
        if type_bot < min:
            type_bot = max
        if type_bot > max:
            type_bot = min
        self.type_bot = type_bot
        self.update_css_for_bot_type_buttons()
        self.inputbox.setFocus()

    def switch_page_widget(self, idx):
        page = self.pages[idx]["Page"]
        self.central.setCurrentWidget(page)

    def initialize_window_size(self):
        self.resize(self.config.WINDOW_W_MIN, self.config.WINDOW_H_MIN)
        self.move(self.window_x_default, self.window_y_default)

    def closeEvent(self, event):
        # ToDo: This does not work as expected.
        # ToDo: Need investigation..
        self.close_app()

    @decorator.app_close_guard
    def close_app(self):
        self.is_app_close = True
        css = self.data_css["button_exit_on"]
        self.button_exit.setStyleSheet(css)
        css = self.data_css["label_bot"]
        self.label_bot.setStyleSheet(css)
        self.label_bot.setTextWithInterval(self.msg_goodby, force_to_write=True)
        self.timers["TimerWorkerCloseApp"].start()

    def save_config_and_close_app(self):
        config_to_json = {}
        config_to_json['WINDOW_X'] = self.x()
        config_to_json['WINDOW_Y'] = self.y()
        config_to_json['WINDOW_W'] = self.width()
        config_to_json['WINDOW_H'] = self.height()
        config_to_json['TYPE_BOT'] = self.type_bot
        self.save_dict_as_json(config_to_json)

    def save_dict_as_json(self, config_to_json):
        text_data_json = json.dumps(
            config_to_json,
            ensure_ascii=False,
            indent=4,
        )
        with open(self.config.PATH_JSON, mode='w', encoding='utf-8') as file:
            file.write(text_data_json)
            file.write('\n')

    @decorator.message_guard_for_input
    def show_msg(self):
        msg_inputbox = self.inputbox.text()
        if len(msg_inputbox) == 0:
            css = self.data_css["label_bot"]
            self.label_bot.setStyleSheet(css)
            self.label_bot.setTextWithInterval(self.msg_warning)
            return

        self.label_you.setTextWithInterval(msg_inputbox)

        if not self.is_bot_ready:
            css = self.data_css["label_bot_ready_ng"]
            self.label_bot.setStyleSheet(css)
            self.label_bot.setTextWithInterval(self.msg_bot_ng)
            return

        self.lister(msg_by_user=msg_inputbox)
        msg_sentence = self.bot.make_sentence(
            starting_token_list=self.lister.get_starting_token_list(),
            token_list=self.lister.get_token_list(),
        )
        msg = f'response: {msg_sentence}'
        self.logger.i(msg)
        css = self.data_css["label_bot"]
        self.label_bot.setStyleSheet(css)
        self.label_bot.setTextWithInterval(msg_sentence)

    @decorator.message_guard_for_bot_not_ready
    def show_bot_not_ready_msg(self):
        css = self.data_css["label_bot_ready_ng"]
        self.label_bot.setStyleSheet(css)
        self.label_bot.setTextWithoutInterval(self.msg_bot_ng)

    @decorator.message_guard_for_bot_ready
    def show_bot_ready_msg(self):
        css = self.data_css["label_bot_ready_ok"]
        self.label_bot.setStyleSheet(css)
        self.label_bot.setTextWithoutInterval(self.msg_bot_ok)

    def update_bot_msg_to_proper_latest_status(self):
        css = self.data_css["label_bot_ready_ok"]
        if css != self.label_bot.get_css():
            self.label_bot.set_css(css)

        txt = self.label_bot.get_response_msg()
        if txt == self.msg_bot_ng:
            self.label_bot.setTextWithoutInterval(self.msg_bot_ok)

    def clear_inputbox(self):
        self.inputbox.clear()

    def play_mouse_click_sound(self):
        idx = 1
        self.play_media[idx].stop()
        self.play_media[idx].play()

    def play_key_press_sound(self):
        idx = 2
        self.play_media[idx].stop()
        self.play_media[idx].play()

    def switch_page_from_button_help(self):
        self.page_idx = 1
        self.switch_page_widget(self.page_idx)

    def switch_page_from_button_back(self):
        self.page_idx = 0
        self.switch_page_widget(self.page_idx)


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
