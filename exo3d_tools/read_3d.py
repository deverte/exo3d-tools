"""Reads 3D (Result.dat) data file."""


import io
import pathlib
import zipfile

import numpy as np

from exo3d_tools.data_3d import Data3D
from exo3d_tools.data_3d import Grid3D
from exo3d_tools.units import EXO3D_UNITS


def _extract_params(text_data: str) -> dict[str, str]:
    lines = text_data.splitlines()

    params = {}
    for line in lines:
        if "arrays" in line:
            break
        key_value = line.split()
        for i, _ in enumerate(key_value):
            if i % 2 == 0:
                params[key_value[i]] = key_value[i + 1]

    return params


def _extract_arrays(
    text_data: str,
    params: dict[str, str],
) -> tuple[dict[str, np.ndarray], np.ndarray]:
    lines = text_data.splitlines()

    arrays_start = 0
    for i, line in enumerate(lines):
        if "arrays" in line:
            arrays_start = i + 1
            break

    arrays = {}
    arrays_lines = lines[arrays_start:]
    for i, line in enumerate(arrays_lines):
        if i % 2 == 0:
            if line != "3D:RFT":
                label = line.split("[")[0]
                if label not in arrays.keys():
                    arrays[label] = []
                arrays[label].append(
                    np.array([float(v) for v in arrays_lines[i + 1].split()])
                )
            else:
                grid_array = np.array([
                    float(v) for v in arrays_lines[i + 1].split()
                ])

    nR = int(params["nR"])
    nF = int(params["nF"])
    for key in arrays.keys():
        shape = (len(arrays[key]), nR + 1, nF + 1)
        arrays[key] = np.array(arrays[key]).reshape(shape).transpose(0, 2, 1)

    return arrays, grid_array


def _extract_grid(
    grid_array: dict[str, np.ndarray],
    params: dict[str, str],
) -> Grid3D:
    nR = int(params["nR"])
    nF = int(params["nF"])
    nTet = int(params["nTet"])

    r_v = np.array([
        grid_array[2 + 2 * (nF + 1)],
        grid_array[2 + 3 * (nF + 1)],
        *[grid_array[0 + j * (nF + 1)] for j in range(2, nR + 1)],
    ])
    r_n = np.array([
        grid_array[3 + 2 * (nF + 1)],
        grid_array[3 + 3 * (nF + 1)],
        *[grid_array[1 + j * (nF + 1)] for j in range(2, nR + 1)],
    ])

    df = 2 * np.pi / nF
    phi_v = np.array([n * df for n in range(nF + 1)])
    phi_n = np.array([n * df for n in range(nF + 1)])

    theta_v = np.array(grid_array[:nTet + 2])
    theta_n = np.array(grid_array[nF + 1:nF + 1 + nTet + 1])

    v = np.meshgrid(theta_v, phi_v, r_v)
    n = np.meshgrid(theta_n, phi_n, r_n)

    return Grid3D(v=v, n=n)


def read_3d_dat(
    file: pathlib.Path | zipfile.Path | io.FileIO | io.BytesIO | io.TextIOBase,
    preserve_grid: bool = True,
) -> Data3D:
    """Reads 3D data (Result.dat) from stream.

    :param file: Stream.
    :param preserve_grid: Preserves original grid (contains service data).
    :return: Data3D.
    """
    if isinstance(file, pathlib.Path):
        text_data = file.read_text()
    elif isinstance(file, zipfile.Path):
        text_data = file.read_text()
    elif issubclass(type(file), io.FileIO):
        text_data = file.read().decode("utf-8")
    elif issubclass(type(file), io.BytesIO):
        text_data = file.getvalue().decode("utf-8")
    elif issubclass(type(file), io.TextIOBase):
        text_data = file.getvalue()
    else:
        raise Exception("Unsupported file type")

    params = _extract_params(text_data)
    arrays, grid_array = _extract_arrays(text_data, params)
    grid = _extract_grid(grid_array, params)
    return Data3D(
        params=params,
        arrays=arrays,
        grid=grid,
        units=EXO3D_UNITS,
        _grid_array=grid_array if preserve_grid else None,
    )