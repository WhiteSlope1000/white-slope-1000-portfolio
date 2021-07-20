from traceback import format_exc as traceback_format_exc
import os
import shutil
from logging import (
    getLogger,
    StreamHandler,
    DEBUG,
    # INFO,
    # WARNING,
    # ERROR,
    # FATAL,
)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Clean(object):
    IS_TEST = 1
    log_level = ''

    def __init__(self):
        if self.log_level != '':
            logger.setLevel(self.log_level)

        logger.warning('')
        logger.warning('')
        msg = 'Start to search unnecessary files ...'
        logger.warning(msg)
        logger.warning('')

        path_crr = os.path.dirname(__file__)
        path_par = os.path.dirname(path_crr)
        for root, dirs, files in os.walk(path_par):
            self.delete_dirs(root, dirs)
            self.delete_files(root, files)
            self.delete_files_by_ext(root, files)

        msg = 'Deleted all found files!'
        logger.warning('')
        logger.warning(msg)
        logger.warning('')

    def delete_dirs(self, root, dirs):
        for dir in dirs[:]:
            flags = (
                dir.startswith('_'),
            )
            if all(flags):
                path = os.path.join(root, dir)
                msg = f'    {dir}: {root}'
                logger.info(msg)
                if self.IS_TEST:
                    continue
                try:
                    shutil.rmtree(path)
                    dirs.remove(dir)
                except (FileNotFoundError, PermissionError):
                    err = '\t#' + traceback_format_exc()
                    err = err.replace('\n', '\n\t#')
                    logger.e(err)

    def delete_files(self, root, files):
        for file in files[:]:
            flags = (
                file != '__init__.py',
                file.startswith('_'),
            )
            if all(flags):
                path = os.path.join(root, file)
                msg = f'    {file}: {root}'
                logger.info(msg)
                if self.IS_TEST:
                    continue
                try:
                    os.remove(path)
                    files.remove(file)
                except (FileNotFoundError, PermissionError):
                    err = '\t#' + traceback_format_exc()
                    err = err.replace('\n', '\n\t#')
                    logger.error(err)

    def delete_files_by_ext(self, root, files):
        for file in files[:]:
            flags = (
                not file.startswith('test'),
                file.endswith('.log'),
            )
            if all(flags):
                path = os.path.join(root, file)
                msg = f'    {file}: {root}'
                logger.info(msg)
                if self.IS_TEST:
                    continue
                try:
                    os.remove(path)
                    files.remove(file)
                except (FileNotFoundError, PermissionError):
                    err = '\t#' + traceback_format_exc()
                    err = err.replace('\n', '\n\t#')
                    logger.error(err)


if __name__ == '__main__':
    Clean.IS_TEST = 1
    Clean()
