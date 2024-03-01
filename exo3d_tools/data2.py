"""2D data."""


from dataclasses import dataclass
from typing import TypeAlias

import numpy as np

import exo3d_tools.data as data
import exo3d_tools.grid2_cartesian as grid2_cartesian
import exo3d_tools.grid2_polar as grid2_polar


_Arr: TypeAlias = "np.ndarray[(nF + 1, nR + 1)]" # type: ignore


@dataclass
class _Data2(data._Data):
    """2D data."""
    #: Data arrays, where dict key is key from `keys`.
    arrays: dict[str, _Arr] = None
    #: Data grid.
    grid: grid2_cartesian.Grid2Cartesian | grid2_polar.Grid2Polar = None