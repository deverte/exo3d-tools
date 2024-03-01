"""3D data."""


from dataclasses import dataclass
import io
import pathlib
from typing import TypeAlias
import zipfile

import numpy as np

import exo3d_tools.data1 as data1
import exo3d_tools.data2_polar as data2_polar
import exo3d_tools.data3 as data3
import exo3d_tools.data3_cartesian as data3_cartesian
import exo3d_tools.grid3_spherical as grid3_spherical
import exo3d_tools.projection31 as projection31
import exo3d_tools.projection32 as projection32
import exo3d_tools.save3 as save3
import exo3d_tools.view3_spherical as view3_spherical


_File: TypeAlias = \
    pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


@dataclass
class Data3Spherical(data3._Data3):
    """3D data."""
    #: Data (densities) grid.
    grid_n: grid3_spherical.Grid3Spherical = None
    #: Data (velocities) grid.
    grid_v: grid3_spherical.Grid3Spherical = None

    def __getitem__(self, key: str) -> view3_spherical._View3Spherical:
        array = self.arrays[key]
        grid = self.grid_n.data
        if np.ravel(array).shape[0] == np.ravel(self.grid_v.data).shape[0]:
            grid = self.grid_v.data
        return view3_spherical._View3Spherical(key=key, array=array, grid=grid)

    def to_1d(self, theta: float = 0, phi: float = 0) -> data1.Data1:
        """Makes projection into Data1D.

        :param theta: Inclination angle from -1.5708 to 1.5708.
        :param phi: Polar angle from 0 to 6.2832.
        :return: Data1D.
        """
        return projection31._projection31(self, theta=theta, phi=phi)

    def to_2d(self, theta: float = 0) -> data2_polar.Data2Polar:
        """Makes projection into Data2D.

        :param theta: Inclination angle from -1.5708 to 1.5708.
        :return: Data2D.
        """
        return projection32._projection32(self, theta=theta)

    def to_cartesian(self) -> "data3_cartesian.Data3Cartesian":
        return data3_cartesian.Data3Cartesian(
            params=self.params,
            arrays=self.arrays,
            grid_n=self.grid_n.to_cartesian(),
            grid_v=self.grid_v.to_cartesian(),
            units=self.units,
            _grid_array=self._grid_array,
        )

    def to_dat(self, file: _File) -> None:
        """Saves data into stream.

        :param file: Output stream.
        """
        save3._save_3d_dat(self, file)