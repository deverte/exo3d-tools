"""1D data."""


from dataclasses import dataclass
from typing import TypeAlias

import numpy as np

import exo3d_tools.plot1 as plot1
import exo3d_tools.view as view


_Arr: TypeAlias = "np.ndarray[(2 * (nR + 1))]" # type: ignore
_Axes: TypeAlias = "matplotlib.axes._axes.Axes" # type: ignore
_Line2D: TypeAlias = "matplotlib.lines.Line2D" # type: ignore


@dataclass
class _View1(view._View):
    """1D data view."""
    #: Data array.
    array: _Arr
    #: Data grid.
    grid: np.ndarray

    def plot(self, ax: _Axes = None, **kwargs) -> list[_Line2D]:
        """Plots 1D data.

        :param ax: Matplotlib axis.
        :return: Matplotlib list[Line2D].
        """
        return plot1._plot_1(self.array, self.grid, ax, **kwargs)