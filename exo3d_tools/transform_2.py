"""2D coordinate transformation."""


import typing

import numpy as np

import exo3d_tools.data_2d as d2


_F: typing.TypeAlias = float | np.ndarray
_Grid2DAny: typing.TypeAlias = "d2.Grid2D | d2.Grid2DYX"


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


def _transform_2_pc(grid: "d2.Grid2D") -> "d2.Grid2DYX":
    r_n = grid.n[1]

    phi_n = grid.n[0]

    theta = grid.theta

    z_n, y_n, x_n = _spherical_to_cartesian(theta, phi_n, r_n)

    n = [y_n, x_n]

    return d2.Grid2DYX(z=z_n, n=n)


def _transform_2_cp(grid: "d2.Grid2DYX") -> "d2.Grid2D":
    x_n = grid.n[1]

    y_n = grid.n[0]

    z = grid.z

    theta_n, phi_n, r_n = _cartesian_to_spherical(z, y_n, x_n)

    n = [phi_n, r_n]

    return d2.Grid2D(theta=theta_n, n=n)


def _mirror_2(grid: _Grid2DAny, axis: typing.Literal["x", "y"]) -> _Grid2DAny:
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

    return d2.Grid2DYX(z=grid.z, n=n)


def _rotate_2(grid: _Grid2DAny, angle: float) -> _Grid2DAny:
    R = np.array([
        [np.cos(angle), np.sin(angle)],
        [-np.sin(angle), np.cos(angle)],
    ])

    n_np = np.einsum("ji, mni -> jmn", R, np.dstack([grid.n[1], grid.n[0]]))
    n = (n_np[0], n_np[1])

    return d2.Grid2DYX(z=grid.z, n=n)