import os
import logging
from rich.logging import RichHandler
FileHandler = logging.FileHandler
StreamHandler = logging.StreamHandler
StreamHandler = RichHandler


class LoggingConst(object):
    LOG_LEVEL_COMMON = logging.DEBUG
    LOG_LEVEL_LOGFILE = logging.DEBUG
    LOG_LEVEL_CONSOLE = logging.INFO

    LOGGER_DIR_LOG = 'logs'
    LOGGER_FILE_TAG = '_'
    LOGGER_FILE_NAME = f'{LOGGER_FILE_TAG}logger'
    LOGGER_FILE_EXTN = '.log'

    LOGGER_FORMAT_DATE = '%H:%M:%S'
    LOGGER_FORMAT_TIME = [
        '%(asctime)s.%(msecs).03d',
    ]
    LOGGER_FORMAT_BASE = [
        # '%(threadName).4s',
        '%(thread)5d',
        # '%(filename)+36s'
        '%(funcName)+28.28s()',
        '%(lineno)3d',
        # '[%(levelname)-8.8s]',
        '%(message)s',
        # 'File "%(filename)s", line %(lineno)s, ',
    ]

    LOGGER_FORMAT_LOGFILE = ' '.join(LOGGER_FORMAT_TIME + LOGGER_FORMAT_BASE)
    LOGGER_FORMAT_CONSOLE = ' '.join(LOGGER_FORMAT_BASE)
    LOGGER_FORMATTER_LOGFILE = logging.Formatter(
        datefmt=LOGGER_FORMAT_DATE, fmt=LOGGER_FORMAT_LOGFILE)
    LOGGER_FORMATTER_CONSOLE = logging.Formatter(
        datefmt=LOGGER_FORMAT_DATE, fmt=LOGGER_FORMAT_CONSOLE)

    # LOGGER_WRAP_WIDTH = 64 * 3


class LoggingBase(object):
    logger = None
    handler_logfile = None
    handler_console = None

    logger_msg_format = '    {2:>32s}: {0:<9s} {1:3d}'.format

    def __init__(self, name_logger='none'):
        self.setup_log_file_path()
        self.setup_new_logger(name_logger)
        self.delete_all_old_log_files()
        self.set_handler_logfile(log_level=self.LOG_LEVEL_LOGFILE)
        self.set_handler_console(log_level=self.LOG_LEVEL_CONSOLE)
        self.set_support_functions()

    def setup_log_file_path(self):
        path_abs = os.path.abspath(__file__)
        path_crr = os.path.dirname(path_abs)
        path_par = os.path.dirname(path_crr)
        path_crr_log = os.path.join(path_crr, self.LOGGER_DIR_LOG)
        path_par_log = os.path.join(path_par, self.LOGGER_DIR_LOG)

        if os.path.exists(path_crr_log):
            self.path_log = path_crr_log
            return

        if os.path.exists(path_par_log):
            self.path_log = path_par_log
            return

        os.mkdir(path_crr_log)
        self.path_log = path_crr_log
        return

    def delete_all_old_log_files(self):
        path_log = self.path_log
        files = os.listdir(path_log)
        for file in files:
            path_file = os.path.join(
                path_log,
                file,
            )

            flag = all((
                file.startswith(self.LOGGER_FILE_TAG),
                file.endswith(self.LOGGER_FILE_EXTN),
            ))
            if not flag:
                continue

            try:
                os.remove(path_file)
            except (PermissionError):
                pass

    def setup_new_logger(self, name_logger):
        if name_logger == 'none':
            name_logger = self.LOGGER_FILE_NAME
        else:
            name_logger = '{}{}'.format(
                self.LOGGER_FILE_TAG,
                name_logger,
            )
        logger = logging.getLogger(name_logger)
        logger.propagate = False
        logger.setLevel(self.LOG_LEVEL_COMMON)
        self.logger = logger

    def set_handler_logfile(self, log_level):
        dargs = self.get_input_args_for_logfile_handler()
        self.handler_logfile = FileHandler(**dargs)
        self.handler_logfile.setLevel(log_level)
        self.handler_logfile.setFormatter(self.LOGGER_FORMATTER_LOGFILE)
        self.logger.addHandler(self.handler_logfile)
        setattr(self.logger, 'handler_logfile', self.handler_logfile)

    def set_handler_console(self, log_level):
        dargs = self.get_input_args_for_console_handler()
        self.handler_console = StreamHandler(**dargs)
        self.handler_console.setLevel(log_level)
        self.handler_console.setFormatter(self.LOGGER_FORMATTER_CONSOLE)
        self.logger.addHandler(self.handler_console)
        setattr(self.logger, 'handler_console', self.handler_console)

        # if 'RichHandler' in str(StreamHandler):
        #    self.handler_console.console.width = self.LOGGER_WRAP_WIDTH

    def get_input_args_for_logfile_handler(self):
        path_log = self.path_log
        basename = '{}{}'.format(
            self.logger.name,
            self.LOGGER_FILE_EXTN,
        )
        fullpath = os.path.join(
            path_log,
            basename,
        )
        dargs = {}
        dargs["filename"] = fullpath
        dargs["mode"] = 'w'
        dargs["encoding"] = 'utf-8'
        return dargs

    def get_input_args_for_console_handler(self):
        dargs = {}
        return dargs

    def set_support_functions(self):
        setattr(self.logger, 'LEVEL_D', logging.DEBUG)
        setattr(self.logger, 'LEVEL_I', logging.INFO)
        setattr(self.logger, 'LEVEL_W', logging.WARNING)
        setattr(self.logger, 'LEVEL_E', logging.ERROR)
        setattr(self.logger, 'LEVEL_F', logging.FATAL)
        setattr(self.logger, 'd', self.logger.debug)
        setattr(self.logger, 'i', self.logger.info)
        setattr(self.logger, 'w', self.logger.warning)
        setattr(self.logger, 'e', self.logger.error)
        setattr(self.logger, 'f', self.logger.fatal)
        setattr(self.logger, 'update_log_levels', self.update_log_levels)
        setattr(self.logger, 'get_all_loggers', self.get_all_loggers)

    def update_log_levels(self, log_level_logfile,
                          log_level_console, log_level_common_='none'):
        self.handler_logfile.setLevel(log_level_logfile)
        self.handler_console.setLevel(log_level_console)

        if log_level_common_ != 'none':
            self.logger.setLevel(log_level_common_)
        log_level_common_ = self.logger.getEffectiveLevel()

        tags = [
            'log_level_logfile',
            'log_level_console',
            'log_level_common ',
        ]
        msgs = [
            'Updated log levels of: "{}" logger'.format(self.logger.name),
            self.logger_msg_format(
                logging.getLevelName(log_level_logfile),
                log_level_logfile,
                tags[0]),
            self.logger_msg_format(
                logging.getLevelName(log_level_console),
                log_level_console,
                tags[1]),
            self.logger_msg_format(
                logging.getLevelName(log_level_common_),
                log_level_common_,
                tags[2]),
        ]
        self.output_msgs_by_fatal(msgs)

    def get_all_loggers(self):
        dat = logging.root.manager.loggerDict
        get = logging.getLogger
        loggers = [get(name) for name in dat]

        msgs = ['Found loggers:']
        for logger in loggers:
            log_level_common_ = logger.getEffectiveLevel()
            tag = '"{}"'.format(logger.name)
            line = self.logger_msg_format(
                logging.getLevelName(log_level_common_),
                log_level_common_,
                tag,
            )
            msgs.append(line)
        self.output_msgs_by_fatal(msgs)
        return loggers

    def output_msgs_by_fatal(self, msgs):
        for msg in msgs:
            self.logger.f(msg)


class Logging(LoggingBase, LoggingConst):
    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    name_logger = 'core_logger'
    logger = Logging(name_logger).get_logger()

    class TestClass(object):
        def __init__(self):
            self.name_logger = name_logger
            self.test01('#### Test "logger.set_support_functions()"')
            self.test02('#### Test "logger.set_support_functions()"')
            self.test03('#### Test "logger.update_log_levels()"')

        def test01(self, msg):
            self.output_by_normal_func(msg)

        def test02(self, msg):
            self.output_by_one_word_func(msg)

        def test03(self, msg):
            logger.update_log_levels(
                log_level_logfile=logger.LEVEL_E,
                log_level_console=logger.LEVEL_E,
            )
            self.output_by_one_word_func(msg)
            logger.update_log_levels(
                log_level_logfile=logger.LEVEL_D,
                log_level_console=logger.LEVEL_D,
            )
            self.output_by_one_word_func(msg)

        def output_by_one_word_func(self, msg):
            logger.f(msg)
            logger.d('One letter func: d')
            logger.i('One letter func: i')
            logger.w('One letter func: w')
            logger.e('One letter func: e')
            logger.f('One letter func: f')
            logger.f('#### End of test')

        def output_by_normal_func(self, msg):
            logger.f(msg)
            logger.debug('Standard func: debug')
            logger.info('Standard func: info')
            logger.warning('Standard func: warning')
            logger.error('Standard func: error')
            logger.fatal('Standard func: fatal')
            logger.f('#### End of test')

    TestClass()
