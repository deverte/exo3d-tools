"""2D data."""


from dataclasses import dataclass
from typing import TypeAlias
from typing import Literal
from typing import Self

import exo3d_tools.view2 as view2
import exo3d_tools.view2_polar as view2_polar
import exo3d_tools.interpolate2 as interpolate2
import exo3d_tools.plot2 as plot2


_Axes: TypeAlias = "matplotlib.axes._axes.Axes" # type: ignore
_QuadMesh: TypeAlias = "matplotlib.collections.QuadMesh" # type: ignore


@dataclass
class _View2Cartesian(view2._View2):
    """2D cartesian data view."""
    def interpolate(
        self,
        size: int = 200,
        r_max: float = None,
    ) -> Self:
        """Interpolates data.

        :param size: X and Y points number.
        :param r_max: Maximal radius.
        :return: _Data2DViewYX.
        """
        return interpolate2._interpolate_2_view(self, size, r_max)

    def mirror(self, axis: Literal["x", "y"]) -> Self:
        """Mirrors data view grid along axis.

        :param axis: Axis to mirror.
        :return: _Data2DViewYX.
        """
        return _View2Cartesian(
            key=self.key,
            array=self.array,
            grid=self.grid.mirror(axis),
        )

    def rotate(self, angle: float) -> Self:
        """Rotates data view grid.

        :param angle: Rotation angle.
        :return: _Data2DViewYX.
        """
        return _View2Cartesian(
            key=self.key,
            array=self.array,
            grid=self.grid.rotate(angle),
        )

    def plot(self, ax: _Axes = None, **kwargs) -> _QuadMesh:
        """Plots 2D data in cartesian grid.

        :param ax: Matplotlib axis (mutable).
        :param shading: Shading type.
        :return: Matplotlib QuadMesh.
        """
        return plot2._plot_2_cartesian(self.array, self.grid, ax, **kwargs)

    def to_polar(self) -> "view2_polar._View2Polar":
        """Converts into 2D data view with polar grid.

        :return: _View2Polar.
        """
        return view2_polar._View2Polar(
            key=self.key,
            array=self.array,
            grid=self.grid.to_polar(),
        )