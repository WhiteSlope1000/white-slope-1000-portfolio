from PyQt5.QtWidgets import (
    QLabel,
)
from common import attach_common
from gui_talkbot_timer import TalkBotTimer
from gui_talkbot_timer_worker import TimerWorkerShowMsg


@attach_common
class QLabelRealTimeWriting(QLabel):
    name = 'TimerWorkerShowMsg'
    add_prefix_to_msg = '{}'.format
    msg_thinking = ''
    msg_response = ''
    css_crr = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_variables()
        self.setup_timer_and_worker()

    def setup_variables(self):
        self.is_writing_msg = False
        self.INTERVAL = self.config.INTERVAL_MSG_SPEED

    def setup_timer_and_worker(self):
        name = self.name

        worker = TimerWorkerShowMsg()
        worker.setObjectName(name)
        worker.daemon = True
        worker.parent = self
        self.worker = worker

        timer = TalkBotTimer()
        timer.setObjectName(name)
        timer.setInterval(self.INTERVAL)
        timer.timeout.connect(worker.run)
        timer.started.connect(worker.setup_worker)
        timer.stopped.connect(worker.clean_worker)
        self.timer = timer

    def get_response_msg(self):
        return self.msg_response

    def get_css(self):
        return self.css_crr

    def set_css(self, css):
        self.css_crr = css
        self.setStyleSheet(css)

    def setTextWithoutInterval(self, msg_response):
        if self.is_writing_msg:
            self.timer.stop()

        self.msg_response = msg_response
        msg = self.add_prefix_to_msg(msg_response)
        self.setText(msg)

    def setTextWithInterval(self, msg_response, force_to_write=False):
        if self.is_writing_msg:
            msg = f'force_to_write: {force_to_write}'
            self.logger.i(msg)
            if force_to_write:
                self.timer.stop()
            else:
                return

        self.msg_response = msg_response
        self.timer.start()


class QLabelBot(QLabelRealTimeWriting):
    name = 'TimerWorkerShowMsgBot'
    add_prefix_to_msg = 'Bot: \n{}'.format
    msg_thinking = '...' + ' ' * 10  # 10 is for time interval (printing 10 spaces)
    msg_response = ''


class QLabelYou(QLabelRealTimeWriting):
    name = 'TimerWorkerShowMsgYou'
    add_prefix_to_msg = 'You: \n{}'.format
    msg_thinking = ''
    msg_response = ''


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    qapp = QApplication(sys.argv)
    QLabelBot()
    QLabelYou()
