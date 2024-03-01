"""Projection from 3D to 1D."""


import exo3d_tools.data1 as data1
import exo3d_tools.data3_spherical as data3_spherical


def _projection31(
    data: "data3_spherical.Data3Spherical",
    theta: float = 0.0,
    phi: float = 0.0,
) -> data1.Data1:
    pr2 = data.to_2d(theta=theta)
    pr1 = pr2.to_1d(phi=phi)
    return pr1
