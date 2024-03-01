"""2D data."""


from dataclasses import dataclass
from typing import TypeAlias

import exo3d_tools.view2 as view2
import exo3d_tools.view2_cartesian as view2_cartesian
import exo3d_tools.plot2 as plot2


_Axes: TypeAlias = "matplotlib.axes._axes.Axes" # type: ignore
_Collection: TypeAlias = "matplotlib.collections.Collection" # type: ignore


@dataclass
class _View2Polar(view2._View2):
    """2D polar data view."""
    def plot(self, ax: _Axes = None, **kwargs) -> _Collection:
        """Plots 2D data in polar grid.

        :param ax: Matplotlib axis (mutable).
        :param shading: Shading type.
        :return: Matplotlib Collection.
        """
        return plot2._plot_2_polar(self.array, self.grid, ax, **kwargs)

    def to_cartesian(self) -> view2_cartesian._View2Cartesian:
        """Converts into 2D data view with cartesian grid.

        :return: _Data2DViewYX.
        """
        return view2_cartesian._View2Cartesian(
            key=self.key,
            array=self.array,
            grid=self.grid.to_cartesian(),
        )