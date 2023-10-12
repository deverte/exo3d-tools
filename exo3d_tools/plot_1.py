"""1D plotting."""


import typing

import numpy as np


def _plot_1(
    array: "np.ndarray[(2 * (nR + 1))]",
    grid: np.ndarray,
    ax: "matplotlib.axes._axes.Axes" = None,
    **kwargs,
) -> "matplotlib.axes._axes.Axes":
    if not ax:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
    ax.plot(grid, array, **kwargs)
    return ax