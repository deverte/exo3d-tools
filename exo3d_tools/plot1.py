"""1D plotting."""


from typing import TypeAlias

import numpy as np


_Arr: TypeAlias = "np.ndarray[(2 * (nR + 1))]" # type: ignore
_Axes: TypeAlias = "matplotlib.axes._axes.Axes" # type: ignore
_Line2D: TypeAlias = "matplotlib.lines.Line2D" # type: ignore


def _plot_1(
    array: _Arr,
    grid: np.ndarray,
    ax: _Axes = None,
    **kwargs,
) -> "list[_Line2D]":
    if not ax:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
    return ax.plot(grid, array, **kwargs)