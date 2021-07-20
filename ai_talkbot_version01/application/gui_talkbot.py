from common import attach_common
from gui_talkbot_main import MainWindowBase
from gui_talkbot_main_func import MainWindowFunc
from gui_talkbot_main_action import (
    MainWindowGuiUserAction,
    MainWindowKeybind,
)


Classes = reversed((
    MainWindowBase,
    MainWindowFunc,
    MainWindowGuiUserAction,
    MainWindowKeybind,
))


@attach_common
class MainWindow(*Classes):
    pass


if __name__ == '__main__':
    TestClass = MainWindow

    import sys
    from PyQt5.QtWidgets import QApplication
    qapp = QApplication(sys.argv)
    window = TestClass()
    window.show()
    code = qapp.exec()
    sys.exit(code)
