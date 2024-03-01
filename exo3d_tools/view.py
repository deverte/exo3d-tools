"""3D data."""


import copy
import dataclasses
from typing import Self

import numpy as np


@dataclasses.dataclass
class _View:
    """Data view."""
    #: Data key.
    key: str
    #: Data array.
    array: np.ndarray
    #: Data grid.
    grid: np.ndarray

    def copy(self) -> Self:
        """Returns copy of the current data view.

        :return: _Data2DView.
        """
        return copy.deepcopy(self)