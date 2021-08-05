import sys
from os.path import dirname, join
path_crr = dirname(__file__)
path_par = dirname(path_crr)
if join(path_par, 'base') not in sys.path:
    sys.path.append(join(path_par, 'base'))
from base_exception import (  # NOQA: E402, F401
    traceback_format_exc,
    AbortProgram,
    NoOverwrittenError,
    ConstError,
    RaiseError,
    TestClass,
)
