"""Reads 1D (scan.dat) data file."""


import io
import pathlib
import zipfile

import numpy as np
import pandas as pd

from exo3d_tools.data_1d import Data1D
from exo3d_tools.data_1d import Grid1D
from exo3d_tools.units import CVIEWER_UNITS


def read_1d_dat(
    file: pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase,
) -> Data1D:
    """Reads 1D data (scan.dat) from stream.

    :param file: Stream.
    :return: Data1D.
    """
    read_csv = lambda buf: pd.read_csv(buf, sep=" ", decimal=",")
    if isinstance(file, pathlib.Path):
        df = read_csv(file)
    elif isinstance(file, zipfile.Path):
        s = io.StringIO(file.read_text("utf-8"))
        df = read_csv(s)
    elif issubclass(type(file), io.FileIO):
        df = read_csv(file)
    elif issubclass(type(file), io.BytesIO):
        b = io.BytesIO(file.getvalue())
        df = read_csv(b)
    elif issubclass(type(file), io.TextIOBase):
        s = io.StringIO(file.getvalue())
        df = read_csv(s)
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
    grid = Grid1D(theta=theta, phi=phi, n=r)

    params = {
        "Rmax": str(r.max()),
        "nR": str(int(df["x"].shape[0] / 2 - 1)),
    }

    return Data1D(params=params, arrays=arrays, grid=grid, units=CVIEWER_UNITS)