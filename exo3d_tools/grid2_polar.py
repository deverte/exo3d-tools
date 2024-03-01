"""2D data."""


from dataclasses import dataclass

import exo3d_tools.grid2 as grid2
import exo3d_tools.grid2_cartesian as grid2_cartesian
import exo3d_tools.transform2 as transform2


@dataclass
class Grid2Polar(grid2._Grid2):
    """2D polar grid."""
    #: Current inclination angle in [-1.5708, 1.5708].
    theta: float

    def to_cartesian(self) -> "grid2_cartesian.Grid2Cartesian":
        """Converts into cartesian grid."""
        return transform2._transform_2_pc(self)