"""Projection from 3D to 2D."""


import numpy as np

import exo3d_tools.data2_polar as data2_polar
import exo3d_tools.data3_spherical as data3_spherical
import exo3d_tools.grid2_polar as grid2_polar


def _projection32(
    data: "data3_spherical.Data3Spherical",
    theta: float = 0.0,
) -> data2_polar.Data2Polar:
    if not -np.pi / 2 <= theta <= np.pi / 2:
        raise Exception("`theta` must be in range [-1.5708, 1.5708]")

    params = data.params
    units = data.units

    theta_n = data.grid_n.data[0][0].T[0]
    theta_v = data.grid_v.data[0][0].T[0]
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

    phi_n = data.grid_n.data[1].T[0][0]
    r_n = data.grid_n.data[2][0][0]
    grid_data = np.meshgrid(phi_n, r_n)
    grid = grid2_polar.Grid2Polar(theta=theta, data=grid_data)

    return data2_polar.Data2Polar(
        params=params,
        arrays=arrays,
        grid=grid,
        units=units,
    )
