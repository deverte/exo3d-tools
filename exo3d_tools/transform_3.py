"""3D coordinate transformation."""


import numpy as np

import exo3d_tools.data_3d as d3


_F = float | np.ndarray


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


def _transform_3_sc(grid: "d3.Grid3D") -> "d3.Grid3DZYX":
    r_v = grid.v[2]
    r_n = grid.n[2]

    phi_v = grid.v[1]
    phi_n = grid.n[1]

    theta_v = grid.v[0]
    theta_n = grid.n[0]

    z_v, y_v, x_v = _spherical_to_cartesian(theta_v, phi_v, r_v)
    z_n, y_n, x_n = _spherical_to_cartesian(theta_n, phi_n, r_n)

    v = [z_v, y_v, x_v]
    n = [z_n, y_n, x_n]

    return d3.Grid3DZYX(v=v, n=n)


def _transform_3_cs(grid: "d3.Grid3DZYX") -> "d3.Grid3D":
    x_v = grid.v[2]
    x_n = grid.n[2]

    y_v = grid.v[1]
    y_n = grid.n[1]

    z_v = grid.v[0]
    z_n = grid.n[0]

    theta_v, phi_v, r_v = _cartesian_to_spherical(z_v, y_v, x_v)
    theta_n, phi_n, r_n = _cartesian_to_spherical(z_n, y_n, x_n)

    v = [theta_v, phi_v, r_v]
    n = [theta_n, phi_n, r_n]

    return d3.Grid3D(v=v, n=n)