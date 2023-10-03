"""2D plotting."""


import typing

import numpy as np


def _plot_2_cartesian(
    array: "np.ndarray[(2 * (nR + 1))]",
    grid: np.ndarray,
    ax: "matplotlib.axes._axes.Axes" = None,
    shading: typing.Literal["auto", "gouraud", "nearest"] = "auto",
) -> "matplotlib.axes._axes.Axes":
    if not ax:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
    x = grid.n[1]
    y = grid.n[0]
    ax.pcolormesh(x, y, array.swapaxes(0, 1), shading=shading)
    return ax


def _plot_2_polar(
    array: "np.ndarray[(2 * (nR + 1))]",
    grid: np.ndarray,
    ax: "matplotlib.axes._axes.Axes" = None,
    shading: typing.Literal["auto", "gouraud", "nearest"] = "auto",
) -> "matplotlib.axes._axes.Axes":
    if not ax:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="polar")
    r = grid.n[1]
    phi = grid.n[0]
    ax.pcolor(phi, r, array.swapaxes(0, 1), shading=shading)
    return ax