"""1D data."""


from dataclasses import dataclass
from typing import Self
from typing import TypeAlias

import numpy as np

import exo3d_tools.grid as grid


_Arr: TypeAlias = "np.ndarray[(nR + 1)]" # type: ignore


@dataclass
class Grid1(grid._Grid):
    """1D grid."""
    #: Current inclination angle in [-1.5708, 1.5708].
    theta: float
    #: Current polar angle in [0, 3.1415].
    phi: float
    #: Distance for densities grid in [planet radius].
    data: _Arr

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, Grid1):
            res = True
            res *= (self.theta == other.theta)
            res *= (self.phi == other.phi)
            res *= (np.around(self.data, 3) == np.around(other.data, 3)).all()
            return res
        return False