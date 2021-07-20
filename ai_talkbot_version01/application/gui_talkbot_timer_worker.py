from PyQt5.QtCore import (
    QObject,
)
from PyQt5.QtCore import pyqtSignal as QSignal  # NOQA: F401
from PyQt5.QtCore import pyqtSlot as QSlot  # NOQA: F401
from common import attach_common


@attach_common
class TimerWorkerBase(QObject):
    parent = None

    def output_start_msg(self):
        msg = 'started "{}"'.format(self.objectName())
        self.logger.i(msg)
        self.get_upper_function_names(activate=0)

    def output_stop_msg(self):
        msg = '        "{}" stopped'.format(self.objectName())
        self.logger.i(msg)
        self.get_upper_function_names(activate=0)

    @QSlot()
    def setup_worker(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    @QSlot()
    def clean_worker(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)


class TimerWorkerCloseApp(TimerWorkerBase):
    @QSlot()
    def setup_worker(self):
        self.output_start_msg()
        self.stop_all_timers()
        self.parent.save_config_and_close_app()

        self.idx = 0
        self.idx_max = self.config.TIMEOUT_APP_CLOSE

    @QSlot()
    def clean_worker(self):
        self.output_stop_msg()
        self.clean_all_timers()

    @QSlot()
    def run(self):
        if self.idx < self.idx_max:
            self.idx += 1
        else:
            self.parent.close()
            self.stop_timer_for_this_worker()

    def stop_timer_for_this_worker(self):
        name = self.objectName()
        self.parent.timers[name].stop()

    def stop_all_timers(self):
        for timer in self.parent.timers.values():
            if timer.objectName() != self.objectName():
                timer.stop()

    def clean_all_timers(self):
        for timer in self.parent.timers.values():
            if timer.objectName() != self.objectName():
                timer.stop()
            timer.deleteLater()


class TimerWorkerShowMsg(TimerWorkerBase):
    @QSlot()
    def setup_worker(self):
        self.output_start_msg()
        self.setup_params()

    @QSlot()
    def clean_worker(self):
        self.output_stop_msg()
        self.reset_params()

    def setup_params(self):
        self.parent.is_writing_msg = True
        self.progress = -1

    def reset_params(self):
        self.parent.is_writing_msg = False
        self.progress = -1

    @QSlot()
    def run(self):
        if self.progress == -1:
            self.prepare_for_output()
            return
        if self.progress == 0:
            self.output_thinking()
            return
        if self.progress == 1:
            self.output_response()
            return
        if self.progress == 2:
            self.stop_timer_for_this_worker()
            return

        raise Exception()

    def prepare_for_output(self):
        self.msg_thinking = self.parent.msg_thinking
        self.msg_response = self.parent.msg_response
        self.idx = 0
        self.idx_max = self.calc_max_idx(self.msg_thinking)
        self.progress = 0
        return

    def output_thinking(self):
        self.logger.d(self.msg_thinking)
        self.logger.d(self.idx)
        if self.idx < self.idx_max:
            msg = self.msg_thinking[:self.idx]
            msg = self.parent.add_prefix_to_msg(msg)
            self.parent.setText(msg)
            self.idx += 1
            return
        self.idx = 0
        self.idx_max = self.calc_max_idx(self.msg_response)
        self.progress = 1
        return

    def output_response(self):
        self.logger.d(self.msg_response)
        self.logger.d(self.idx)
        if self.idx < self.idx_max:
            msg = self.msg_response[:self.idx]
            msg = self.parent.add_prefix_to_msg(msg)
            self.parent.setText(msg)
            self.idx += 1
            return
        self.idx = 0
        self.idx_max = 0
        self.progress = 2
        return

    def calc_max_idx(self, msg):
        idx_interval = 10
        idx_max = len(msg)
        idx_max = idx_max + idx_interval if idx_max != 0 else 0
        return idx_max

    def clean_timer_for_this_worker(self):
        self.stop_timer_for_this_worker()
        self.delete_timer_for_this_worker()

    def stop_timer_for_this_worker(self):
        self.parent.timer.stop()

    def delete_timer_for_this_worker(self):
        self.parent.timer.deleteLater()


if __name__ == "__main__":
    TestClass = TimerWorkerCloseApp()

    from gui_talkbot import MainWindow
    TestClass = MainWindow

    import sys
    from PyQt5.QtWidgets import QApplication
    qapp = QApplication(sys.argv)
    window = TestClass()
    window.show()
    code = qapp.exec()
    sys.exit(code)
