import sys
import path_setter  # NOQA: F401
import application.core_all_file_cleaner_in_real  # NOQA: F401
from application.gui_talkbot import MainWindow
from PyQt5.QtWidgets import QApplication

qapp = QApplication(sys.argv)
window = MainWindow()
window.show()
code = qapp.exec()
sys.exit(code)
