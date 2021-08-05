import sys
from os.path import dirname, join
path_crr = dirname(__file__)
path_par = dirname(path_crr)
path_par = dirname(path_par)
if join(path_par, 'base') not in sys.path:
    sys.path.append(join(path_par, 'base'))
from base_full_half import ZenHan  # NOQA: E402, F401
