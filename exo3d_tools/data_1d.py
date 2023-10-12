"""1D data."""


import _collections_abc
import copy
from dataclasses import dataclass
from dataclasses import field
import io
import pathlib
import zipfile

import numpy as np
import pandas as pd

from exo3d_tools.convert import _convert
from exo3d_tools.dataframe_1 import _dataframe_1
from exo3d_tools.plot_1 import _plot_1
from exo3d_tools.save_1d import _save_1d_dat
from exo3d_tools.units import _UnitsType
from exo3d_tools.units import Units


_File = pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


@dataclass
class Grid1D:
    """1D grid."""
    #: Current inclination angle in [-1.5708, 1.5708].
    theta: float
    #: Current polar angle in [0, 3.1415].
    phi: float
    #: Distance for densities grid in [planet radius].
    n: "np.ndarray[(nR + 1)]"

    def __eq__(self, other: "Grid1D") -> bool:
        if isinstance(other, Grid1D):
            res = True
            res *= (self.theta == other.theta)
            res *= (self.phi == other.phi)
            res *= (np.around(self.n, 4) == np.around(other.n, 4)).all()
            return res
        return False


@dataclass
class _Data1DView:
    """1D data view."""
    #: Data key.
    key: str
    #: Data array.
    array: "np.ndarray[(2 * (nR + 1))]"
    #: Data grid.
    grid: np.ndarray

    def plot(
        self,
        ax: "matplotlib.axes._axes.Axes" = None,
        **kwargs,
    ) -> "matplotlib.axes._axes.Axes":
        """Plots 1D data.

        :param ax: Matplotlib axis (mutable).
        :return: Matplotlib axis (reference to `ax`).
        """
        return _plot_1(self.array, self.grid, ax, **kwargs)


@dataclass
class Data1D:
    """1D data."""
    #: Parameters.
    params: dict[str, str]
    #: Data arrays, where dict key is key from `keys`.
    arrays: dict[str, "np.ndarray[(2 * (nR + 1))]"]
    #: Data grid.
    grid: Grid1D
    #: Units.
    units: Units = field(
        default_factory=lambda: Units(
            density="cm-3",
            temperature="K",
            velocity="km s-1",
            distance="km",
        ),
    )

    def __eq__(self, other: "Data1D") -> bool:
        if isinstance(other, Data1D):
            res = True
            for key in set(self.params.keys()) & set(other.params.keys()):
                res *= (self.params[key] == other.params[key])
            res *= (self.keys() == other.keys())
            for key in self.keys():
                res *= (
                    np.around(self.arrays[key], 4) ==
                    np.around(other.arrays[key], 4)
                ).all()
            res *= (self.grid == other.grid)
            res *= (self.units == other.units)
            return res
        return False

    def __getitem__(self, key: str) -> _Data1DView:
        return _Data1DView(key=key, array=self.arrays[key], grid=self.grid.n)

    def convert(self, f: _UnitsType | Units) -> "Data1D":
        """Converts physical units.

        :param f: Final units.
        :return: Data1D.
        """
        return _convert(self, f)

    def copy(self) -> "Data1D":
        """Returns copy of current object.

        :return: Data1D.
        """
        return copy.deepcopy(self)

    def keys(self) -> _collections_abc.dict_keys:
        """Returns data keys.

        :return: Data1D.
        """
        return self.arrays.keys()

    def to_dat(self, file: _File) -> None:
        """Saves data into stream.

        :param file: Output stream.
        """
        _save_1d_dat(self, file)

    def to_dataframe(self) -> pd.DataFrame:
        """Represents data as Pandas DataFrame.

        :return: pandas.DataFrame.
        """
        return _dataframe_1(self)