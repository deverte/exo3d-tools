"""3D data."""


import _collections_abc
import copy
from dataclasses import dataclass
from dataclasses import field
from typing import Self

import numpy as np

import exo3d_tools.convert as convert
import exo3d_tools.grid as grid
import exo3d_tools.units as us


@dataclass
class _Data:
    """Data."""
    #: Parameters.
    params: dict[str, str] = None
    #: Data arrays, where dict key is key from `keys`.
    arrays: dict[str, np.ndarray] = None
    #: Units.
    units: us.Units = field(
        default_factory=lambda: us.Units(
            density="cm-3",
            temperature="K",
            velocity="km s-1",
            distance="km",
        ),
    )

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, _Data):
            res = True
            for key in set(self.params.keys()) & set(other.params.keys()):
                res *= (self.params[key] == other.params[key])
            res *= (self.keys() == other.keys())
            for key in self.keys():
                res *= (
                    np.around(self.arrays[key], 3) ==
                    np.around(other.arrays[key], 3)
                ).all()
            res *= (self.grid == other.grid)
            res *= (self.units == other.units)
            return res
        return False

    def convert(self, f: us._UnitsType | us.Units) -> Self:
        """Converts physical units.

        :param f: Final units.
        :return: Data3D.
        """
        return convert._convert(self, f)

    def copy(self) -> Self:
        """Returns copy of current object.

        :return: Data3D.
        """
        return copy.deepcopy(self)

    def keys(self) -> _collections_abc.dict_keys:
        """Returns data keys.

        :return: Data3D.
        """
        return self.arrays.keys()