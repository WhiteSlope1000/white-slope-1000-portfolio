from PyQt5.QtCore import (
    QTimer,
)
from PyQt5.QtCore import pyqtSignal as QSignal  # NOQA: F401
from PyQt5.QtCore import pyqtSlot as QSlot  # NOQA: F401


class TalkBotTimer(QTimer):
    started = QSignal()
    stopped = QSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
        self.started.emit()

    def stop(self, *args, **kwargs):
        super().stop(*args, **kwargs)
        self.stopped.emit()


if __name__ == '__main__':
    from PyQt5.QtCore import (
        QObject,
    )
    from PyQt5.QtWidgets import (
        QMainWindow,
        QGridLayout,
        QWidget,
        QVBoxLayout,
        QPushButton,
    )
    from common import attach_common

    class TestClassBase(QMainWindow):
        def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)
            self.make_widget()
            self.setup_widget()
            self.setup_layout()
            self.setup_window()
            self.setup_timer_and_worker()
            self.setup_signal_connection()

        def make_widget(self):
            self.page_central = QWidget()
            self.layout_central = QGridLayout()
            self.label = QVBoxLayout()
            self.button = QPushButton()

        def setup_widget(self):
            self.button.setText('start timer to push here')

        def setup_layout(self):
            self.label.addWidget(self.button)
            self.layout_central.addLayout(self.label, 0, 0)
            self.page_central.setLayout(self.layout_central)
            self.setCentralWidget(self.page_central)

        def setup_window(self):
            self.setWindowTitle('test')
            self.setMinimumSize(640, 480)

        def setup_timer_and_worker(self):
            pass

        def setup_signal_connection(self):
            pass

    class TestWorker(QObject):
        parent = None

        @QSlot()
        def run(self):
            self.parent.button.setText('timer test is OK!')

    @attach_common
    class TestClass(TestClassBase):
        timer = None
        worker = None

        def setup_timer_and_worker(self):
            self.timer = TalkBotTimer()
            self.timer.start()

            name = 'TestWorker'
            worker = TestWorker()
            worker.setObjectName(name)
            worker.daemon = True
            worker.parent = self
            self.worker = worker

        def setup_signal_connection(self):
            self.button.clicked.connect(self.start_timer)

        def start_timer(self):
            self.timer.timeout.connect(self.worker.run)
            self.timer.start(1000)
            self.logger.w('timer start!')

        def stop_func(self):
            self.timer.stop()

    inst = TestClass

    import sys
    from PyQt5.QtWidgets import QApplication
    qapp = QApplication(sys.argv)
    window = inst()
    window.show()
    code = qapp.exec()
    sys.exit(code)
