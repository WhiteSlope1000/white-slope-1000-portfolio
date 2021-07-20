from traceback import format_exc as traceback_format_exc
from core_logger import Logging
logger = Logging(__name__).get_logger()


class RaiseError(object):
    def __init__(self, *args, **kwargs):
        flags = (
            'ExceptionClass' in kwargs,
            'name' in kwargs,
        )
        if all(flags):
            name = kwargs["name"]
            Class = kwargs["ExceptionClass"]
            if name == '__main__':
                name = Class.__name__
                msg = f'{name}: OK because of test.'
                logger.e(msg)
            else:
                raise Class()


class AbortProgram(Exception):
    pass


class NoOverwrittenError(Exception):
    pass


class InvalidNumOfNgramError(Exception):
    pass


if __name__ == '__main__':
    TestClasses = (
        AbortProgram,
        NoOverwrittenError,
        InvalidNumOfNgramError,
    )

    for TestClass in TestClasses:
        try:
            err = '!!!!'
            raise TestClass(err)
        except TestClass:
            err = traceback_format_exc()
            logger.e(err)

    for TestClass in TestClasses:
        RaiseError(name=__name__, ExceptionClass=TestClass)

    for TestClass in TestClasses:
        try:
            RaiseError(name='test', ExceptionClass=TestClass)
        except TestClass:
            err = traceback_format_exc()
            logger.e(err)
