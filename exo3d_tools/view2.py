"""2D data."""


from dataclasses import dataclass
from typing import TypeAlias

import numpy as np

import exo3d_tools.view as view


_Arr: TypeAlias = "np.ndarray[(nF + 1, nR + 1)]" # type: ignore


@dataclass
class _View2(view._View):
    """2D polar data view."""
    #: Data array.
    array: _Arr