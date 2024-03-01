"""3D data."""


from dataclasses import dataclass

import exo3d_tools.grid3 as grid3
import exo3d_tools.grid3_cartesian as grid3_cartesian
import exo3d_tools.transform3 as transform3


@dataclass
class Grid3Spherical(grid3._Grid3):
    """Cartesian grid."""
    def to_cartesian(self) -> "grid3_cartesian.Grid3Cartesian":
        """Converts into cartesian grid.

        :return: Grid3DZYX.
        """
        return transform3._transform_3_sc(self)