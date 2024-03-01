"""2D coordinate transformation."""


from typing import Literal
from typing import TypeAlias

import numpy as np

import exo3d_tools.grid2_cartesian as grid2_cartesian
import exo3d_tools.grid2_polar as grid2_polar


_F: TypeAlias = float | np.ndarray
_Grid2Any: TypeAlias = \
    "grid2_cartesian.Grid2Cartesian | grid2_polar.Grid2Polar"


def _spherical_to_cartesian(theta: _F, phi: _F, r: _F) -> tuple[_F, _F, _F]:
    x = r * np.sin(theta + np.pi / 2) * np.cos(phi)
    y = r * np.sin(theta + np.pi / 2) * np.sin(phi)
    z = r * np.cos(theta + np.pi / 2)
    return z, y, x


def _cartesian_to_spherical(z: _F, y: _F, x: _F) -> tuple[_F, _F, _F]:
    r = np.sqrt(x**2 + y**2 + z**2)
    phi = np.arctan2(-y, -x) + np.pi
    theta = np.arccos(z / r) - np.pi / 2.0
    return theta, phi, r


def _transform_2_pc(
    grid: "grid2_polar.Grid2Polar",
) -> "grid2_cartesian.Grid2Cartesian":
    r_n = grid.data[1]

    phi_n = grid.data[0]

    theta = grid.theta

    z_n, y_n, x_n = _spherical_to_cartesian(theta, phi_n, r_n)

    n = [y_n, x_n]

    return grid2_cartesian.Grid2Cartesian(z=z_n, data=n)


def _transform_2_cp(
    grid: "grid2_cartesian.Grid2Cartesian",
) -> "grid2_polar.Grid2Polar":
    x_n = grid.data[1]

    y_n = grid.data[0]

    z = grid.z

    theta_n, phi_n, r_n = _cartesian_to_spherical(z, y_n, x_n)

    n = [phi_n, r_n]

    return grid2_polar.Grid2Polar(theta=theta_n, data=n)


def _mirror_2(grid: _Grid2Any, axis: Literal["x", "y"]) -> _Grid2Any:
    if axis == "x":
        R = np.array([
            [1, 0],
            [0, -1],
        ])
    elif axis == "y":
        R = np.array([
            [-1, 0],
            [0, 1],
        ])

    n_np = np.einsum("ji, mni -> jmn", R, np.dstack([grid.n[1], grid.n[0]]))
    n = (n_np[0], n_np[1])

    return grid2_cartesian.Grid2Cartesian(z=grid.z, data=n)


def _rotate_2(grid: _Grid2Any, angle: float) -> _Grid2Any:
    R = np.array([
        [np.cos(angle), np.sin(angle)],
        [-np.sin(angle), np.cos(angle)],
    ])

    n_np = np.einsum("ji, mni -> jmn", R, np.dstack([grid.n[1], grid.n[0]]))
    n = (n_np[0], n_np[1])

    return grid2_cartesian.Grid2Cartesian(z=grid.z, data=n)