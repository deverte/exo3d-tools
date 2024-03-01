"""3D data."""


from dataclasses import dataclass
from typing import TypeAlias

import numpy as np

import exo3d_tools.view as view


_Arr: TypeAlias = \
    "np.ndarray[(nTet + grid_1_or_2, nF + 1, nR + 1)]" # type: ignore


@dataclass
class _View3(view._View):
    """3D cartesian data view."""
    #: Data array.
    array: _Arr