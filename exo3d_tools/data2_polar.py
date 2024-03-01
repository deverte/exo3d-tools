"""2D data."""


import dataclasses

import exo3d_tools.data1 as data1
import exo3d_tools.data2 as data2
import exo3d_tools.data2_cartesian as data2_cartesian
import exo3d_tools.grid2_polar as grid2_polar
import exo3d_tools.projection21 as projection21
import exo3d_tools.view2_polar as view2_polar


@dataclasses.dataclass
class Data2Polar(data2._Data2):
    """2D data."""
    #: Data grid.
    grid: grid2_polar.Grid2Polar = None

    def __getitem__(self, key: str) -> view2_polar._View2Polar:
        return view2_polar._View2Polar(
            key=key,
            array=self.arrays[key],
            grid=self.grid,
        )

    def to_1d(self, phi: float = 0) -> data1.Data1:
        return projection21._projection21(self, phi=phi)

    def to_polar(self) -> "data2_cartesian.Data2Cartesian":
        return data2_cartesian.Data2Cartesian(
            params=self.params,
            arrays=self.arrays,
            grid=self.grid.to_cartesian(),
            units=self.units,
        )