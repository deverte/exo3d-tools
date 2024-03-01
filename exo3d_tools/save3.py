"""Saves 3D (Result.dat) data file."""


import io
import pathlib
import zipfile
from typing import TypeAlias

import numpy as np

import exo3d_tools.data3_cartesian as data3_cartesian
import exo3d_tools.data3_spherical as data3_spherical
import exo3d_tools.units as units


_File: TypeAlias = \
    pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase


def _save_3d_dat(data: "data3_spherical.Data3Spherical", file: _File) -> None:
    data = data.copy().convert(units.EXO3D_UNITS)

    text_data = ""
    for key, value in data.params.items():
        text_data += f"{key} {value}\n"

    text_data += "arrays 0\n"
    for key, arrays in data.arrays.items():
        for i, array in enumerate(arrays):
            text_data += f"{key}[{i}]\n"
            text_data += " ".join(str(s) for s in array.T.flatten()) + " \n"

    text_data += "3D:RFT\n"
    if data._grid_array:
        text_data += " ".join(str(s) for s in data._grid_array) + " \n"
    else:
        theta_v = data.grid_v.data[0][0].T[0]
        phi_v = data.grid_v.data[1].T[0][0]
        r_v = data.grid_v.data[2][0][0]
        theta_n = data.grid_n.data[0][0].T[0]
        r_n = data.grid_n.data[2][0][0]

        grid = np.zeros((r_v.shape[0], phi_v.shape[0]))
        grid[0][:theta_v.shape[0]] = theta_v
        grid[1][:theta_n.shape[0]] = theta_n
        grid[2][2] = r_v[0]
        grid[2][3] = r_n[0]
        grid[3][2] = r_v[1]
        grid[3][3] = r_n[1]
        grid.T[0][2:] = r_v[2:]
        grid.T[1][2:] = r_n[2:]

        text_data += " ".join(str(s) for s in grid.flatten()) + " \n"

    if isinstance(file, pathlib.Path):
        file.write_text(text_data, encoding="utf-8")
    elif isinstance(file, zipfile.Path):
        with file.open(mode="w") as f:
            f.write(text_data)
    elif issubclass(type(file), io.FileIO):
        file.write(str.encode(text_data))
    elif issubclass(type(file), io.BytesIO):
        file.write(str.encode(text_data))
    elif issubclass(type(file), io.TextIOBase):
        file.write(text_data)
    else:
        raise Exception("Unsopported file type")


def _save_3d_cartesian_csv(
    data: "data3_cartesian.Data3Cartesian",
    file: _File,
) -> None:
    df = data.to_dataframe_cartesian()

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