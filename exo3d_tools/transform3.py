"""3D coordinate transformation."""


import numpy as np

import exo3d_tools.grid3_cartesian as grid3_cartesian
import exo3d_tools.grid3_spherical as grid3_spherical


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


def _transform_3_sc(
    grid: "grid3_spherical.Grid3Spherical",
) -> "grid3_cartesian.Grid3Cartesian":
    r = grid.data[2]
    phi = grid.data[1]
    theta = grid.data[0]

    z, y, x = _spherical_to_cartesian(theta, phi, r)

    data = [z, y, x]

    return grid3_cartesian.Grid3Cartesian(data=data)


def _transform_3_cs(
    grid: "grid3_cartesian.Grid3Cartesian",
) -> "grid3_spherical.Grid3Spherical":
    x = grid.data[2]
    y = grid.data[1]
    z = grid.data[0]

    theta, phi, r = _cartesian_to_spherical(z, y, x)

    data = [theta, phi, r]

    return grid3_spherical.Grid3Spherical(data=data)