from PyQt5.QtGui import (
    QPainter,
)
from PyQt5.QtWidgets import (
    QWidget,
    QStyle,
    QStyleOption,
)
from common import attach_common


@attach_common
class PageBase(object):
    def paintEvent(self, event):
        # This hack is for making css-setting of QWidget valid.
        option = QStyleOption()
        option.initFrom(self)
        paint = QPainter(self)
        self.style().drawPrimitive(
            QStyle.PE_Widget,
            option,
            paint,
            self,
        )


class QPage00(PageBase, QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QPage01(PageBase, QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    qapp = QApplication(sys.argv)
    QPage00()
    QPage01()
