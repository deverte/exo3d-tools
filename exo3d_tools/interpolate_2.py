"""2D interpolation."""


import numpy as np
from scipy.interpolate import LinearNDInterpolator


def _interpolate_2(
    data: "exo3d_tools._Data2DViewYX",
    size: int = 200,
    r_max: float = None,
) -> "exo3d_tools._Data2DViewYX":
    data = data.copy()

    if not r_max:
        r_max = data.grid.n.max()

    x_grid = data.grid.n[1]
    y_grid = data.grid.n[0]
    pairs = np.array([y_grid, x_grid]).T.reshape(-1, 2)
    v_min = data.array.min()
    interp = LinearNDInterpolator(pairs, data.array.flat, fill_value=v_min)

    x = np.linspace(-r_max, r_max, size)
    y = np.linspace(-r_max, r_max, size)
    y_mesh, x_mesh = np.meshgrid(y, x)
    array = interp(y_mesh, x_mesh).swapaxes(0, 1)

    data.grid.n = (y_mesh, x_mesh)
    data.array = array

    return data