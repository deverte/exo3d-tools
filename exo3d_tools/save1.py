"""Saves 1D (scan.dat) data file."""


import io
import pathlib
import zipfile
from typing import TypeAlias

import exo3d_tools.data1 as data1


_File: TypeAlias = \
    pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


def _save_1d_csv(data: "data1.Data1", file: _File) -> None:
    df = data.to_dataframe()

    save = lambda buf: df.to_csv(
        buf,
        index=False,
        float_format="%.4e",
    )
    if isinstance(file, pathlib.Path):
        save(file)
    elif isinstance(file, zipfile.Path):
        with file.open(mode="w") as f:
            save(f)
    elif issubclass(type(file), io.FileIO):
        save(file)
    elif issubclass(type(file), io.BytesIO):
        save(file)
    elif issubclass(type(file), io.TextIOBase):
        save(file)
    else:
        raise Exception("Unsopported file type")