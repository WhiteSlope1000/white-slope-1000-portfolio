import sys
from os.path import dirname, join
path_crr = dirname(__file__)
path_par = dirname(path_crr)
path_par = dirname(path_par)
if join(path_par, 'base') not in sys.path:
    sys.path.append(join(path_par, 'base'))
import all_file_cleaner  # NOQA: E402, F401
