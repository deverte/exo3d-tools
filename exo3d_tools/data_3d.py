"""3D data."""


import _collections_abc
import copy
from dataclasses import dataclass
from dataclasses import field
import io
import pathlib
import zipfile

import numpy as np

from exo3d_tools.convert import _convert
from exo3d_tools.data_1d import Data1D
from exo3d_tools.data_2d import Data2D
from exo3d_tools.projection_3_2 import _projection_3_2
from exo3d_tools.projection_3_1 import _projection_3_1
from exo3d_tools.save_3d import _save_3d_dat
from exo3d_tools.transform_3 import _transform_3_cs
from exo3d_tools.transform_3 import _transform_3_sc
from exo3d_tools.units import _UnitsType
from exo3d_tools.units import Units


_File = pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


@dataclass
class Grid3D:
    """Spherical grid."""
    #: Meshgrid for velocities grid.
    #: Inclination angle for velocities grid in [-1.5708, 1.5708].
    #: Polar angle for velocities grid in [0, 6.2832].
    #: Distance for velocities grid in [planet radius].
    v: list["np.ndarray[(nTet + 2, nF + 1, nR + 1)]"]
    #: Meshgrid for densities grid.
    #: Inclination angle for densities grid in [-1.5708, 1.5708].
    #: Polar angle for densities grid in [0, 6.2832].
    #: Distance for densities grid in [planet radius].
    n: list["np.ndarray[(nTet + 1, nF + 1, nR + 1)]"]

    def __eq__(self, other: "Grid3D") -> bool:
        if isinstance(other, Grid3D):
            res = True
            for i in len(self.n):
                res *= (
                    np.around(self.n[i], 4) == np.around(other.n[i], 4)
                ).all()
            for i in len(self.v):
                res *= (
                    np.around(self.v[i], 4) == np.around(other.v[i], 4)
                ).all()
            return res
        return False

    def to_cartesian(self) -> "Grid3DZYX":
        """Converts into cartesian grid.

        :return: Grid3DZYX.
        """
        return _transform_3_sc(self)


@dataclass
class Grid3DZYX:
    """Cartesian grid."""
    #: Meshgrid for velocities grid.
    #: Inclination angle for velocities grid in [-1.5708, 1.5708].
    #: Polar angle for velocities grid in [0, 6.2832].
    #: Distance for velocities grid in [planet radius].
    v: list["np.ndarray[(nTet + 2, nF + 1, nR + 1)]"]
    #: Meshgrid for densities grid.
    #: Inclination angle for densities grid in [-1.5708, 1.5708].
    #: Polar angle for densities grid in [0, 6.2832].
    #: Distance for densities grid in [planet radius].
    n: list["np.ndarray[(nTet + 1, nF + 1, nR + 1)]"]

    def to_spherical(self) -> Grid3D:
        """Converts into spherical grid.

        :return: Grid3D.
        """
        return _transform_3_cs(self)


@dataclass
class Data3D:
    """3D data."""
    #: Parameters.
    params: dict[str, str]
    #: Data arrays, where dict key is key from `keys`.
    arrays: dict[str, "np.ndarray[(nTet + 1 | nTet + 2, nF + 1, nR + 1)]"]
    #: Data grid.
    grid: Grid3D
    #: Units.
    units: Units = field(
        default_factory=lambda: Units(
            density="cm-3",
            temperature="K",
            velocity="km s-1",
            distance="km",
        ),
    )
    #: Grid array. Needed to perserve service data.
    _grid_array: np.ndarray | None = None

    def __eq__(self, other: "Data3D") -> bool:
        if isinstance(other, Data3D):
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

    def convert(self, f: _UnitsType | Units) -> "Data3D":
        """Converts physical units.

        :param f: Final units.
        :return: Data3D.
        """
        return _convert(self, f)

    def copy(self) -> "Data3D":
        """Returns copy of current object.

        :return: Data3D.
        """
        return copy.deepcopy(self)

    def keys(self) -> _collections_abc.dict_keys:
        """Returns data keys.

        :return: Data3D.
        """
        return self.arrays.keys()

    def to_dat(self, file: _File) -> None:
        """Saves data into stream.

        :param file: Output stream.
        """
        _save_3d_dat(self, file)

    def to_2d(self, theta: float = 0) -> Data2D:
        """Makes projection into Data2D.

        :param theta: Inclination angle from -1.5708 to 1.5708.
        :return: Data2D.
        """
        return _projection_3_2(self, theta=theta)

    def to_1d(self, theta: float = 0, phi: float = 0) -> Data1D:
        """Makes projection into Data1D.

        :param theta: Inclination angle from -1.5708 to 1.5708.
        :param phi: Polar angle from 0 to 6.2832.
        :return: Data1D.
        """
        return _projection_3_1(self, theta=theta, phi=phi)