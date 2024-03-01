"""3D data."""


from dataclasses import dataclass
import io
import pathlib
from typing import TypeAlias
import zipfile

import numpy as np

import exo3d_tools.data1 as data1
import exo3d_tools.data2_cartesian as data2_cartesian
import exo3d_tools.data3 as data3
import exo3d_tools.data3_spherical as data3_spherical
import exo3d_tools.grid3_cartesian as grid3_cartesian
import exo3d_tools.view3_cartesian as view3_cartesian


_File: TypeAlias = \
    pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


@dataclass
class Data3Cartesian(data3._Data3):
    """3D data."""
    #: Data (densities) grid.
    grid_n: grid3_cartesian.Grid3Cartesian = None
    #: Data (velocities) grid.
    grid_v: grid3_cartesian.Grid3Cartesian = None

    def __getitem__(self, key: str) -> view3_cartesian._View3Cartesian:
        array = self.arrays[key]
        grid = self.grid_n.data
        if np.ravel(array).shape[0] == np.ravel(self.grid_v.data).shape[0]:
            grid = self.grid_v.data
        return view3_cartesian._View3Cartesian(key=key, array=array, grid=grid)

    def to_1d(self, z: float = 0, y: float = 0) -> data1.Data1:
        raise NotImplementedError()

    def to_2d(self, z: float = 0) -> data2_cartesian.Data2Cartesian:
        raise NotImplementedError()

    def to_dat(self, file: _File) -> None:
        self.to_spherical().to_dat(file)

    def to_spherical(self) -> data3_spherical.Data3Spherical:
        return data3_spherical.Data3Spherical(
            params=self.params,
            arrays=self.arrays,
            grid_n=self.grid_n.to_spherical(),
            grid_v=self.grid_v.to_spherical(),
            units=self.units,
            _grid_array=self._grid_array,
        )