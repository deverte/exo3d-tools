"""1D data."""


from dataclasses import dataclass
import io
import pathlib
import zipfile
from typing import TypeAlias
from typing import Self

import numpy as np
import pandas as pd

import exo3d_tools.data as data
import exo3d_tools.dataframe1 as dataframe1
import exo3d_tools.grid1 as grid1
import exo3d_tools.save1 as save1
import exo3d_tools.view1 as view1


_Arr: TypeAlias = "np.ndarray[(2 * (nR + 1))]" # type: ignore
_File = pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


@dataclass
class Data1(data._Data):
    """1D data."""
    #: Data arrays, where dict key is key from `keys`.
    arrays: dict[str, _Arr] = None
    #: Data grid.
    grid: grid1.Grid1 = None

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, Data1):
            res = True
            for key in set(self.params.keys()) & set(other.params.keys()):
                res *= (self.params[key] == other.params[key])
            res *= (self.keys() == other.keys())
            for key in self.keys():
                res *= (
                    np.around(self.arrays[key], 3) ==
                    np.around(other.arrays[key], 3)
                ).all()
            res *= (self.grid == other.grid)
            res *= (self.units == other.units)
            return res
        return False

    def __getitem__(self, key: str) -> view1._View1:
        return view1._View1(
            key=key,
            array=self.arrays[key],
            grid=self.grid.data,
        )

    def to_csv(self, file: _File) -> None:
        """Saves data into stream.

        :param file: Output stream.
        """
        save1._save_1d_csv(self, file)

    def to_dataframe(self) -> pd.DataFrame:
        """Represents data as Pandas DataFrame.

        :return: pandas.DataFrame.
        """
        return dataframe1._dataframe_1(self)