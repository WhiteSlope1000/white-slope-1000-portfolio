import sys
from os.path import dirname, join
path_crr = dirname(__file__)
path_par = dirname(path_crr)
if join(path_par, 'base') not in sys.path:
    sys.path.append(join(path_par, 'base'))
from base_logger import Logging  # NOQA: E402, F401
