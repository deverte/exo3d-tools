"""Saves 3D (Result.dat) data file."""


import io
import pathlib
import zipfile

import numpy as np

from exo3d_tools.units import EXO3D_UNITS


def _save_3d_dat(
    data: "Data3D",
    file: pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase,
) -> None:
    data = data.copy().convert(EXO3D_UNITS)

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
        theta_v = data.grid.v[0][0].T[0]
        phi_v = data.grid.v[1].T[0][0]
        r_v = data.grid.v[2][0][0]
        theta_n = data.grid.n[0][0].T[0]
        r_n = data.grid.n[2][0][0]

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