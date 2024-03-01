"""2D data."""


from dataclasses import dataclass
from typing import Self
from typing import TypeAlias

import numpy as np

import exo3d_tools.grid as grid


_Arr: TypeAlias = "np.ndarray[(nF + 1, nR + 1)]" # type: ignore


@dataclass
class _Grid2(grid._Grid):
    """2D polar grid."""
    #: Meshgrid for densities grid.
    #: Polar angle for densities grid in [0, 6.2832].
    #: Distance for densities grid in [planet radius].
    data: list[_Arr]

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, _Grid2):
            res = True
            res *= (self.theta == other.theta)
            for i in len(self.data):
                res *= (
                    np.around(self.data[i], 3) == np.around(other.data[i], 3)
                ).all()
            return res
        return False