import os.path
import sys
import re
from inspect import currentframe
from traceback import extract_stack as traceback_extract_stack
from config import AiConfig
from core_exception import (
    traceback_format_exc,  # NOQA: F401
    RaiseError,
    AbortProgram,
    NoOverwrittenError,
    InvalidNumOfNgramError,
)
from core_logger import Logging
name_logger = __name__
logger = Logging(name_logger).get_logger()

name_root_py = 'start_application.py'
if name_root_py in sys.argv[0]:
    logger.update_log_levels(
        log_level_logfile=logger.LEVEL_E,
        log_level_console=logger.LEVEL_E,
    )


class AiInterface(object):
    config = AiConfig()


class AiModules(object):
    traceback_format_exc = traceback_format_exc
    logger = logger
    sys = sys

    RaiseError = RaiseError
    AbortProgram = AbortProgram
    NoOverwrittenError = NoOverwrittenError
    InvalidNumOfNgramError = InvalidNumOfNgramError


class AiCommomFuncDebugPurpose(object):
    @classmethod
    def output_members(cls):
        for name in dir(cls):
            cls.logger.i(name)

    def link_currentframe_func(self):
        self.get_current_frame = currentframe

    def get_func_name(self, frame):
        # Original usage: sys._getframe().f_code.co_name
        # Aiming of this function:
        #   self.link_currentframe_func()
        #   name_frame = self.get_current_frame()
        #   name_func = self.get_func_name(name_frame)
        return frame.f_code.co_name

    def get_upper_function_names(self, activate=0):
        if not activate:
            return

        msgs = []
        stacks = traceback_extract_stack(limit=10)
        max = len(stacks) - 1
        for idx in reversed(range(0, max)):
            level = (max - (idx + 1))
            name_func = stacks[idx][2]
            numb_line = stacks[idx][1]
            path_file = stacks[idx][0]
            msgs.append("TraceLevel{:2d}: '{:48s}' {}:{}".format(
                level,
                name_func + str('()'),
                os.path.basename(path_file),
                numb_line,
            ))
        msgs.append('')

        msgs[0] = f'{msgs[0]} is debug point.'
        for line in msgs:
            self.logger.i(line)


class AiCommomFunc(object):
    def sort_chr_type(self, chr):
        if re.match('[ぁ-ん]', chr):
            chr_type = 0
        elif re.match('[ァ-ン]', chr):
            chr_type = 1
        elif re.match('[ー-鵈]', chr):
            chr_type = 2
        else:
            chr_type = 3
        return chr_type

    def get_trailing_characters(self):
        try:
            self.characters_trailing
        except AttributeError:
            self.characters_trailing = (
                '。',
                '.',
                '！',
                '!',
                '？',
                '?',
            )
        return self.characters_trailing


Classes = reversed((
    AiInterface,
    AiModules,
    AiCommomFuncDebugPurpose,
    AiCommomFunc,
))


class AiCommom(*Classes):
    pass


def attach_common(cls_target):
    cls_source = AiCommom
    msg = 'Attaching from "{}" to "{}":'.format(
        cls_source.__name__,
        cls_target,
    )
    logger.w(msg)

    names_source = dir(cls_source)
    names_target = dir(cls_target)
    for name in names_source:
        if name.startswith('__'):
            msg = f'Skipped: {name}'
            logger.d(msg)
            continue

        if name in names_target:
            msg = f'Duplicated: {name}'
            logger.d(msg)
            continue

        attr = getattr(cls_source, name)
        setattr(cls_target, name, attr)
        msg = f'Attached: {name}'
        logger.d(msg)
    return cls_target


if __name__ == '__main__':
    logger.update_log_levels(
        log_level_logfile=logger.LEVEL_D,
        log_level_console=logger.LEVEL_D,
    )

    @attach_common
    class TestClass(object):
        def switch_function(self, msg):
            def inner(msg):
                self.logger.i(f'{msg}: inner')

            self.logger.i(f'{msg}: switch_function')
            self.link_currentframe_func()
            name_frame = self.get_current_frame()
            name_func = self.get_func_name(name_frame)
            setattr(self, name_func, inner)

    inst = TestClass()
    inst.output_members()
    try:
        inst.config.WINDOW_H_MIN = 0
    except inst.config.ConstError:
        err = 'ConstError: OK because of test mode.'
        logger.e(err)
    try:
        inst.config.WINDOW_HOGE = 0
    except inst.config.ConstError:
        err = 'ConstError: OK because of test mode.'
        logger.e(err)

    inst.switch_function('1st')
    inst.switch_function('2nd')
