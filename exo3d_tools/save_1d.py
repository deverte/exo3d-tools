"""Saves 1D (scan.dat) data file."""


import io
import pathlib
import zipfile

import numpy as np
import pandas as pd

from exo3d_tools.units import CVIEWER_UNITS


def _save_1d_dat(
    data: "Data1D",
    file: pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase,
) -> None:
    df = data.to_dataframe()

    save = lambda buf: df.to_csv(
        buf,
        sep=" ",
        index=False,
        decimal=",",
        float_format="%.4f",
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