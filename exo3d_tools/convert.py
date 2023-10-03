"""Physical conversion functions."""


import numpy as np

from exo3d_tools.units import _DensityUnit
from exo3d_tools.units import _DistanceUnit
from exo3d_tools.units import _TemperatureUnit
from exo3d_tools.units import _VelocityUnit
from exo3d_tools.units import _UnitsType
from exo3d_tools.units import Units


def _convert_temperature(
    array: np.ndarray,
    f: _TemperatureUnit,
    i: _TemperatureUnit,
) -> np.ndarray:
    t = {"1e4 K": 1.0e-4, "K": 1.0}
    output = t[f] / t[i] * array
    return output


def _convert_velocity(
    array: np.ndarray,
    f: _VelocityUnit,
    i: _VelocityUnit,
) -> np.ndarray:
    v = {"9.07 km s-1": 1.0 / (9.07), "km s-1": 1.0}
    output = v[f] / v[i] * array
    return output


def _convert_distance(
    array: np.ndarray,
    f: _DistanceUnit,
    i: _DistanceUnit,
    planet_radius: float = 1.0, # Planet radius [Jupiter radius]
) -> np.ndarray:
    JUPITER_RADIUS = 7.1492e4
    r = {
        "planet radius": 1.0 / JUPITER_RADIUS,
        "Jupiter radius": 1.0 / (planet_radius * JUPITER_RADIUS),
        "km": 1.0,
    }
    output = r[f] / r[i] * array
    return output


def _convert_density(
    array: np.ndarray,
    f: _DensityUnit,
    i: _DensityUnit,
) -> np.ndarray:
    n = {
        "lg(cm-3)": {
            "lg(cm-3)": lambda arr: arr,
            "cm-3": lambda arr: 10.0**arr,
        },
        "cm-3": {
            "lg(cm-3)": lambda arr: np.log10(arr),
            "cm-3": lambda arr: arr,
        },
    }
    output = n[i][f](array)
    return output


def _convert(
    data: "exo3d_tools.Data1D | exo3d_tools.Data2D | exo3d_tools.Data3D",
    f: _UnitsType | Units,
) -> "exo3d_tools.Data1D | exo3d_tools.Data2D | exo3d_tools.Data3D":
    data = data.copy()

    if not isinstance(f, Units):
        f = Units(density=f[0], temperature=f[1], velocity=f[2], distance=f[3])
    i = data.units

    for key in data.arrays.keys():
        if ".Tn" in key:
            data.arrays[key] = _convert_temperature(
                data.arrays[key],
                f.temperature,
                i.temperature,
            )
        elif (".Vr" in key) or (".Vt" in key) or (".Vf" in key):
            data.arrays[key] = _convert_velocity(
                data.arrays[key],
                f.velocity,
                i.velocity,
            )
        else:
            data.arrays[key] = _convert_density(
                data.arrays[key],
                f.density,
                i.density,
            )

    Rplanet = float(data.params.get("Rplanet", 1.0))
    cd = lambda arr: _convert_distance(
        arr,
        f.distance,
        i.distance,
        planet_radius=Rplanet,
    )
    if len(data.grid.n) == 3:
        data.grid.n[2] = cd(data.grid.n[2])
        data.grid.v[2] = cd(data.grid.v[2])
    elif len(data.grid.n) == 2:
        data.grid.n[1] = cd(data.grid.n[1])
        data.grid.v[1] = cd(data.grid.v[1])
    elif len(data.grid.n) == 1:
        data.grid.n[0] = cd(data.grid.n[0])
        data.grid.v[0] = cd(data.grid.v[0])

    data.units = f
    return data