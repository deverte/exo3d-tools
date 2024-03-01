"""3D data."""


import exo3d_tools.view3 as view3
import exo3d_tools.view3_cartesian as view3_cartesian


class _View3Spherical(view3._View3):
    """3D spherical data view."""
    def to_cartesian(self) -> "view3_cartesian._View3Cartesian":
        """Converts into 2D data view with cartesian grid.

        :return: _Data2DViewYX.
        """
        return view3_cartesian._View3Cartesian(
            key=self.key,
            array=self.array,
            grid=self.grid.to_cartesian(),
        )