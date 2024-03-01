"""2D data."""


from dataclasses import dataclass
from typing import Literal
from typing import Self

import exo3d_tools.grid2 as grid2
import exo3d_tools.grid2_polar as grid2_polar
import exo3d_tools.transform2 as transform2


@dataclass
class Grid2Cartesian(grid2._Grid2):
    """2D cartesian grid."""
    #: Z coordinate in [planet radius].
    z: float

    def mirror(self, axis: Literal["x", "y"]) -> Self:
        """Mirrors grid along axis.

        :param axis: Axis to mirror.
        :return: Grid2DYX.
        """
        return transform2._mirror_2(self, axis=axis)

    def rotate(self, angle: float) -> Self:
        """Rotates grid.

        :param angle: Rotation angle.
        :return: Grid2DYX.
        """
        return transform2._rotate_2(self, angle=angle)

    def to_polar(self) -> "grid2_polar.Grid2Polar":
        """Converts into polar grid.

        :return: Grid2D.
        """
        return transform2._transform_2_cp(self)