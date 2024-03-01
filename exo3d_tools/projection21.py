"""Projection from 2D to 1D."""


import numpy as np

import exo3d_tools.data2_polar as data2_polar
import exo3d_tools.data1 as data1
import exo3d_tools.grid1 as grid1


def _projection21(
    data: "data2_polar.Data2Polar",
    phi: float = 0.0,
) -> data1.Data1:
    if not 0.0 <= phi <= np.pi:
        raise Exception("`phi` must be in range [0, 3.1415]")

    theta = data.grid.theta
    params = data.params
    units = data.units

    phi_n = data.grid.data[0][0]
    phi_n_index_minus = np.argmin(np.abs(phi_n - (phi + np.pi)))
    phi_n_index_plus = np.argmin(np.abs(phi_n - phi))

    arrays = {}
    for key in data.keys():
        array_minus = np.flip(data.arrays[key][phi_n_index_minus])
        array_plus = data.arrays[key][phi_n_index_plus]
        arrays[key] = np.concatenate((array_minus, array_plus))

    n_plus = data.grid.data[1].T[0]
    n_minus = -np.flip(n_plus)
    grid_data = np.concatenate((n_minus, n_plus))
    grid = grid1.Grid1(theta=theta, phi=phi, data=grid_data)

    return data1.Data1(
        params=params,
        arrays=arrays,
        grid=grid,
        units=units,
    )