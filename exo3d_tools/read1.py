"""Reads 1D (scan.dat) data file."""


import io
import pathlib
import zipfile
from typing import TypeAlias

import numpy as np
import pandas as pd

import exo3d_tools.data1 as data1
import exo3d_tools.grid1 as grid1
import exo3d_tools.units as units


_File: TypeAlias = \
    pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


def read_1d_csv(file: _File) -> data1.Data1:
    """Reads 1D data (scan.dat) from stream.

    :param file: Stream.
    :return: Data1D.
    """
    if isinstance(file, pathlib.Path):
        df = pd.read_csv(file)
    elif isinstance(file, zipfile.Path):
        s = io.StringIO(file.read_text("utf-8"))
        df = pd.read_csv(s)
    elif issubclass(type(file), io.FileIO):
        df = pd.read_csv(file)
    elif issubclass(type(file), io.BytesIO):
        b = io.BytesIO(file.getvalue())
        df = pd.read_csv(b)
    elif issubclass(type(file), io.TextIOBase):
        s = io.StringIO(file.getvalue())
        df = pd.read_csv(s)
    else:
        raise Exception("Unsupported file type")

    arrays = {}
    for key in df.keys()[3:]:
        arrays[key] = df[key].to_numpy()

    x = df["x"].to_numpy()
    y = df["Y"].to_numpy()
    z = df["Z"].to_numpy()
    r = np.sqrt(x**2 + y**2 + z**2)
    r[:int(r.shape[0] / 2)] = -r[:int(r.shape[0] / 2)]
    phi = np.arctan2(y[0], x[0]) + np.pi
    theta = np.arccos(z[0] / r[0]) - np.pi / 2.0
    grid = grid1.Grid1(theta=theta, phi=phi, data=r)

    params = {
        "Rmax": str(r.max()),
        "nR": str(int(df["x"].shape[0] / 2 - 1)),
    }

    return data1.Data1(
        params=params,
        arrays=arrays,
        grid=grid,
        units=units.CVIEWER_UNITS,
    )