"""3D data."""


from dataclasses import dataclass
from typing import Self
from typing import TypeAlias

import numpy as np

import exo3d_tools.grid as grid


_Arr: TypeAlias = \
    "np.ndarray[(nTet + 1 | nTet + 2, nF + 1, nR + 1)]" # type: ignore


@dataclass
class _Grid3(grid._Grid):
    """Grid 3D."""
    data: list[_Arr]

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, _Grid3):
            res = True
            for i in len(self.data):
                res *= (
                    np.around(self.data[i], 3) == np.around(other.data[i], 3)
                ).all()
            return res
        return False