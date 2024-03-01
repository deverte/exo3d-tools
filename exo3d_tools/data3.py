"""3D data."""


from dataclasses import dataclass
from typing import TypeAlias

import numpy as np

import exo3d_tools.data as data
import exo3d_tools.grid3_cartesian as grid3_cartesian
import exo3d_tools.grid3_spherical as grid3_spherical


_ArrV: TypeAlias = "np.ndarray[(nTet + 2, nF + 1, nR + 1)]" # type: ignore
_ArrN: TypeAlias = "np.ndarray[(nTet + 1, nF + 1, nR + 1)]" # type: ignore


@dataclass
class _Data3(data._Data):
    """3D data."""
    #: Data arrays, where dict key is key from `keys`.
    arrays: dict[str, "_ArrV | _ArrN"] = None
    #: Data (densities) grid.
    grid_n: grid3_cartesian.Grid3Cartesian | grid3_spherical.Grid3Spherical = \
        None
    #: Data (velocities) grid.
    grid_v: grid3_cartesian.Grid3Cartesian | grid3_spherical.Grid3Spherical = \
        None
    #: Grid array. Needed to perserve service data.
    _grid_array: np.ndarray | None = None