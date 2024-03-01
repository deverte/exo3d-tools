"""3D data."""


from dataclasses import dataclass

import exo3d_tools.grid3 as grid3
import exo3d_tools.grid3_spherical as grid3_spherical
import exo3d_tools.transform3 as transform3


@dataclass
class Grid3Cartesian(grid3._Grid3):
    """Cartesian grid."""
    def to_spherical(self) -> grid3_spherical.Grid3Spherical:
        """Converts into spherical grid.

        :return: Grid3D.
        """
        return transform3._transform_3_cs(self)