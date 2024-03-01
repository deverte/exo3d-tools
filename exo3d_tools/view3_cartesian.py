"""3D data."""


from dataclasses import dataclass
import pathlib
import io
import zipfile
from typing import TypeAlias

import pandas as pd

import exo3d_tools.view3 as view3
import exo3d_tools.view3_spherical as view3_spherical
import exo3d_tools.save3 as save3
import exo3d_tools.dataframe3 as dataframe3


_File: TypeAlias = \
    pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


@dataclass
class _View3Cartesian(view3._View3):
    """3D cartesian data view."""
    def to_csv(self, file: _File) -> None:
        """Saves data into stream.

        :param file: Output stream.
        """
        save3._save_3d_cartesian_csv(self, file)

    def to_dataframe(self) -> pd.DataFrame:
        """Represents data as Pandas DataFrame.

        :return: pandas.DataFrame.
        """
        return dataframe3._dataframe_3_cartesian(self)

    def to_polar(self) -> "view3_spherical._View3Spherical":
        """Converts into 2D data view with polar grid.

        :return: _Data2DView.
        """
        return view3_spherical._View3Spherical(
            key=self.key,
            array=self.array,
            grid=self.grid.to_spherical(),
        )