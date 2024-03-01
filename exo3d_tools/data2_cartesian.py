"""2D data."""


import dataclasses

import exo3d_tools.data1 as data1
import exo3d_tools.data2 as data2
import exo3d_tools.data2_polar as data2_polar
import exo3d_tools.grid2_cartesian as grid2_cartesian
import exo3d_tools.view2_cartesian as view2_cartesian


@dataclasses.dataclass
class Data2Cartesian(data2._Data2):
    """2D data."""
    #: Data grid.
    grid: grid2_cartesian.Grid2Cartesian = None

    def __getitem__(self, key: str) -> view2_cartesian._View2Cartesian:
        return view2_cartesian._View2Cartesian(
            key=key,
            array=self.arrays[key],
            grid=self.grid,
        )

    def to_1d(self, y: float = 0) -> data1.Data1:
        raise NotImplementedError()

    def to_polar(self) -> "data2_polar.Data2Polar":
        return data2_polar.Data2Polar(
            params=self.params,
            arrays=self.arrays,
            grid=self.grid.to_polar(),
            units=self.units,
        )