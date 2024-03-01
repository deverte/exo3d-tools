"""2D interpolation."""


import numpy as np
from scipy.interpolate import LinearNDInterpolator

import exo3d_tools.data2_cartesian as data2_cartesian


def _interpolate_2_view(
    data: "data2_cartesian.Data2Cartesian",
    size: int = 200,
    r_max: float = None,
) -> "data2_cartesian.Data2Cartesian":
    data = data.copy()

    if not r_max:
        r_max = data.grid.n.max()

    x_grid = data.grid.data[1]
    y_grid = data.grid.data[0]
    pairs = np.array([y_grid, x_grid]).T.reshape(-1, 2)
    v_min = data.array.min()
    interp = LinearNDInterpolator(pairs, data.array.flat, fill_value=v_min)

    x = np.linspace(-r_max, r_max, size)
    y = np.linspace(-r_max, r_max, size)
    y_mesh, x_mesh = np.meshgrid(y, x)
    array = interp(y_mesh, x_mesh).swapaxes(0, 1)

    data.grid.data = (y_mesh, x_mesh)
    data.array = array

    return data