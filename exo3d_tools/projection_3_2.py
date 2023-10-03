"""Projection from 3D to 2D."""


import numpy as np

from exo3d_tools.data_2d import Data2D
from exo3d_tools.data_2d import Grid2D


def _projection_3_2(data: "exo3d_tools.Data3D", theta: float = 0.0) -> Data2D:
    if not -np.pi / 2 <= theta <= np.pi / 2:
        raise Exception("`theta` must be in range [-1.5708, 1.5708]")

    params = data.params
    units = data.units

    theta_n = data.grid.n[0][0].T[0]
    theta_v = data.grid.v[0][0].T[0]
    theta_n_index = np.argmin(np.abs(theta_n - theta))
    theta_v_index = np.argmin(np.abs(theta_v - theta))
    theta_index = {
        theta_n.shape[0]: theta_n_index,
        theta_v.shape[0]: theta_v_index,
    }

    arrays = {}
    for key in data.keys():
        theta_idx = theta_index[data.arrays[key].shape[0]]
        arrays[key] = data.arrays[key][theta_idx]

    phi_n = data.grid.n[1].T[0][0]
    r_n = data.grid.n[2][0][0]
    n = np.meshgrid(phi_n, r_n)
    grid = Grid2D(theta=theta, n=n)

    return Data2D(
        params=params,
        arrays=arrays,
        grid=grid,
        units=units,
    )
