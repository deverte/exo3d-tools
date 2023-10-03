"""Projection from 3D to 1D."""


from exo3d_tools.data_1d import Data1D


def _projection_3_1(
    data: "exo3d_tools.Data3D",
    theta: float = 0.0,
    phi: float = 0.0,
) -> Data1D:
    pr2 = data.to_2d(theta=theta)
    pr1 = pr2.to_1d(phi=phi)
    return pr1
