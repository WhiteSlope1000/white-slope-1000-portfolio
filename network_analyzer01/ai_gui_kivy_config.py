from core_exception import ConstError
from core_const import Const
from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '64')
Config.set('graphics', 'borderless', 'True')


class ConfigAddon(Const):
    INTERVAL_ENTER = 0.2  # sec
    BG_COLOR = [0.8, 0.8, 0.8, 1.0]
    CURSOR_WIDTH = 8
    CURSOR_COLOR = [0, 0, 1, 1]
    FONT_SIZE = 18


if __name__ == '__main__':
    config = ConfigAddon()
    try:
        config.TITLE = 0
    except ConstError:
        err = 'ConstError: OK because of test mode.'
        print(err)

    try:
        config.FONT = 0
    except ConstError:
        err = 'ConstError: OK because of test mode.'
        print(err)
