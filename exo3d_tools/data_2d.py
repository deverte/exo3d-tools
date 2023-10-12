"""2D data."""


import _collections_abc
import copy
from dataclasses import dataclass
from dataclasses import field
import typing

import numpy as np

from exo3d_tools.convert import _convert
from exo3d_tools.data_1d import Data1D
from exo3d_tools.interpolate_2 import _interpolate_2
from exo3d_tools.plot_2 import _plot_2_cartesian
from exo3d_tools.plot_2 import _plot_2_polar
from exo3d_tools.projection_2_1 import _projection_2_1
from exo3d_tools.transform_2 import _mirror_2
from exo3d_tools.transform_2 import _rotate_2
from exo3d_tools.transform_2 import _transform_2_cp
from exo3d_tools.transform_2 import _transform_2_pc
from exo3d_tools.units import _UnitsType
from exo3d_tools.units import Units


@dataclass
class Grid2D:
    """2D polar grid."""
    #: Current inclination angle in [-1.5708, 1.5708].
    theta: float
    #: Meshgrid for densities grid.
    #: Inclination angle for densities grid in [-1.5708, 1.5708].
    #: Polar angle for densities grid in [0, 6.2832].
    #: Distance for densities grid in [planet radius].
    n: list["np.ndarray[(nF + 1, nR + 1)]"]

    def to_cartesian(self) -> "Grid2DYX":
        """Converts into cartesian grid."""
        return _transform_2_pc(self)

    def __eq__(self, other: "Grid2D") -> bool:
        if isinstance(other, Grid2D):
            res = True
            res *= (self.theta == other.theta)
            for i in len(self.n):
                res *= (
                    np.around(self.n[i], 4) == np.around(other.n[i], 4)
                ).all()
            return res
        return False


@dataclass
class Grid2DYX:
    """2D cartesian grid."""
    #: Z coordinate in [planet radius].
    z: float
    #: Meshgrid for densities grid.
    #: Polar angle for densities grid in [0, 6.2832].
    #: Distance for densities grid in [planet radius].
    n: list["np.ndarray[(nF + 1, nR + 1)]"]

    def mirror(self, axis: typing.Literal["x", "y"]) -> "Grid2DYX":
        """Mirrors grid along axis.

        :param axis: Axis to mirror.
        :return: Grid2DYX.
        """
        return _mirror_2(self, axis=axis)

    def rotate(self, angle: float) -> "Grid2DYX":
        """Rotates grid.

        :param angle: Rotation angle.
        :return: Grid2DYX.
        """
        return _rotate_2(self, angle=angle)

    def to_polar(self) -> Grid2D:
        """Converts into polar grid.

        :return: Grid2D.
        """
        return _transform_2_cp(self)


@dataclass
class _Data2DView:
    """2D polar data view."""
    #: Data key.
    key: str
    #: Data array.
    array: "np.ndarray[(nF + 1, nR + 1)]"
    #: Data grid.
    grid: Grid2D

    def copy(self) -> "_Data2DView":
        """Returns copy of the current data view.

        :return: _Data2DView.
        """
        return copy.deepcopy(self)

    def plot(
        self,
        ax: "matplotlib.axes._axes.Axes" = None,
        **kwargs,
    ) -> "matplotlib.axes._axes.Axes":
        """Plots 2D data in polar grid.

        :param ax: Matplotlib axis (mutable).
        :param shading: Shading type.
        :return: Matplotlib axis (reference to `ax`).
        """
        return _plot_2_polar(self.array, self.grid, ax, **kwargs)

    def to_cartesian(self) -> "_Data2DViewYX":
        """Converts into 2D data view with cartesian grid.

        :return: _Data2DViewYX.
        """
        return _Data2DViewYX(
            key=self.key,
            array=self.array,
            grid=self.grid.to_cartesian(),
        )


@dataclass
class _Data2DViewYX:
    """2D cartesian data view."""
    #: Data key.
    key: str
    #: Data array.
    array: "np.ndarray[(nF + 1, nR + 1)]"
    #: Data grid.
    grid: Grid2DYX

    def copy(self) -> "_Data2DViewYX":
        """Returns copy of the current data view.

        :return: _Data2DViewYX.
        """
        return copy.deepcopy(self)

    def interpolate(
        self,
        size: int = 200,
        r_max: float = None,
    ) -> "_Data2DViewYX":
        """Interpolates data.

        :param size: X and Y points number.
        :param r_max: Maximal radius.
        :return: _Data2DViewYX.
        """
        return _interpolate_2(self, size, r_max)

    def mirror(self, axis: typing.Literal["x", "y"]) -> "_Data2DViewYX":
        """Mirrors data view grid along axis.

        :param axis: Axis to mirror.
        :return: _Data2DViewYX.
        """
        return _Data2DViewYX(
            key=self.key,
            array=self.array,
            grid=self.grid.mirror(axis),
        )

    def rotate(self, angle: float) -> "_Data2DViewYX":
        """Rotates data view grid.

        :param angle: Rotation angle.
        :return: _Data2DViewYX.
        """
        return _Data2DViewYX(
            key=self.key,
            array=self.array,
            grid=self.grid.rotate(angle),
        )

    def plot(
        self,
        ax: "matplotlib.axes._axes.Axes" = None,
        **kwargs,
    ) -> "matplotlib.axes._axes.Axes":
        """Plots 2D data in cartesian grid.

        :param ax: Matplotlib axis (mutable).
        :param shading: Shading type.
        :return: Matplotlib axis (reference to `ax`).
        """
        return _plot_2_cartesian(self.array, self.grid, ax, **kwargs)

    def to_polar(self) -> _Data2DView:
        """Converts into 2D data view with polar grid.

        :return: _Data2DView.
        """
        return _Data2DView(
            key=self.key,
            array=self.array,
            grid=self.grid.to_polar(),
        )


@dataclass
class Data2D:
    """2D data."""
    #: Parameters.
    params: dict[str, str]
    #: Data arrays, where dict key is key from `keys`.
    arrays: dict[str, "np.ndarray[(nF + 1, nR + 1)]"]
    #: Data grid.
    grid: Grid2D
    #: Units.
    units: Units = field(
        default_factory=lambda: Units(
            density="cm-3",
            temperature="K",
            velocity="km s-1",
            distance="km",
        ),
    )

    def __eq__(self, other: "Data2D") -> bool:
        if isinstance(other, Data2D):
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

    def __getitem__(self, key: str) -> _Data2DView:
        return _Data2DView(key=key, array=self.arrays[key], grid=self.grid)

    def convert(self, f: _UnitsType | Units) -> "Data2D":
        """Converts physical units.

        :param f: Final units.
        :return: Data2D.
        """
        return _convert(self, f)

    def copy(self) -> "Data2D":
        """Returns copy of current object.

        :return: Data2D.
        """
        return copy.deepcopy(self)

    def keys(self) -> _collections_abc.dict_keys:
        """Returns data keys.

        :return: Data2D.
        """
        return self.arrays.keys()

    def to_1d(self, phi: float = 0) -> Data1D:
        """Makes projection into Data1D.

        :param phi: Polar angle from 0 to 6.2832.
        :return: Data1D.
        """
        return _projection_2_1(self, phi=phi)