"""Projection from 2D to 1D."""


import numpy as np

from exo3d_tools.data_1d import Data1D
from exo3d_tools.data_1d import Grid1D


def _projection_2_1(data: "exo3d_tools.Data2D", phi: float = 0.0) -> Data1D:
    if not 0.0 <= phi <= np.pi:
        raise Exception("`phi` must be in range [0, 3.1415]")

    theta = data.grid.theta
    params = data.params
    units = data.units

    phi_n = data.grid.n[0][0]
    phi_n_index_minus = np.argmin(np.abs(phi_n - (phi + np.pi)))
    phi_n_index_plus = np.argmin(np.abs(phi_n - phi))

    arrays = {}
    for key in data.keys():
        array_minus = np.flip(data.arrays[key][phi_n_index_minus])
        array_plus = data.arrays[key][phi_n_index_plus]
        arrays[key] = np.concatenate((array_minus, array_plus))

    n_plus = data.grid.n[1].T[0]
    n_minus = -np.flip(n_plus)
    n = np.concatenate((n_minus, n_plus))
    grid = Grid1D(theta=theta, phi=phi, n=n)

    return Data1D(
        params=params,
        arrays=arrays,
        grid=grid,
        units=units,
    )