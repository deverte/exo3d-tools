"""2D plotting."""


from typing import TypeAlias

import numpy as np


_Arr: TypeAlias = "np.ndarray[(2 * (nR + 1))]" # type: ignore
_Axes: TypeAlias = "matplotlib.axes._axes.Axes" # type: ignore
_Collection: TypeAlias = "matplotlib.collections.Collection" # type: ignore
_QuadMesh: TypeAlias = "matplotlib.collections.QuadMesh" # type: ignore


def _plot_2_cartesian(
    array: _Arr,
    grid: np.ndarray,
    ax: _Axes = None,
    **kwargs,
) -> _QuadMesh:
    if not ax:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
    x = grid.data[1]
    y = grid.data[0]
    return ax.pcolormesh(x, y, array.swapaxes(0, 1), **kwargs)


def _plot_2_polar(
    array: _Arr,
    grid: np.ndarray,
    ax: _Axes = None,
    **kwargs,
) -> _Collection:
    if not ax:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="polar")
    r = grid.data[1]
    phi = grid.data[0]
    return ax.pcolor(phi, r, array.swapaxes(0, 1), **kwargs)