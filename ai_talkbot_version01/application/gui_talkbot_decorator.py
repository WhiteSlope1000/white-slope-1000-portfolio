import time


class Decorator(object):
    def bot_change_guard(self, func):
        def core(inst, type_bot):
            if inst.is_app_close:
                return
            if not inst.is_bot_ready:
                return
            func(inst, type_bot)
            return
        return core

    def message_guard_for_input(self, func):
        def core(inst):
            if inst.is_app_close:
                return
            if not inst.is_bot_ready:
                return
            func(inst)
            return
        return core

    def message_guard_for_bot_not_ready(self, func):
        def core(inst):
            flags = (
                inst.is_app_close is True,
                inst.is_bot_ready is True,
            )
            if any(flags):
                return
            func(inst)
            return
        return core

    def message_guard_for_bot_ready(self, func):
        def core(inst):
            flags = (
                inst.is_app_close is True,
                inst.is_bot_ready is False,
            )
            if any(flags):
                return
            func(inst)
            return
        return core

    def app_close_guard(self, func):
        def core(inst):
            if inst.is_app_close:
                return
            func(inst)
            return
        return core

    def elapse_time_measurement(self, func):
        def core(inst):
            time_sta = time.time()
            func(inst)
            time_end = time.time()

            time_dif = time_end - time_sta
            msg = f'elapse time: {time_dif:1.3f} [sec] {func}'
            inst.logger.i(msg)
            return
        return core


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
