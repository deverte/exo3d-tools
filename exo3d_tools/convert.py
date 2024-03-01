"""Physical conversion functions."""


import numpy as np

import exo3d_tools.data as data
import exo3d_tools.units as units


def _convert_temperature(
    array: np.ndarray,
    f: units._TemperatureUnit,
    i: units._TemperatureUnit,
) -> np.ndarray:
    t = {"1e4 K": 1.0e-4, "K": 1.0}
    output = t[f] / t[i] * array
    return output


def _convert_velocity(
    array: np.ndarray,
    f: units._VelocityUnit,
    i: units._VelocityUnit,
) -> np.ndarray:
    v = {"9.07 km s-1": 1.0 / (9.07), "km s-1": 1.0}
    output = v[f] / v[i] * array
    return output


def _convert_distance(
    array: np.ndarray,
    f: units._DistanceUnit,
    i: units._DistanceUnit,
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
    f: units._DensityUnit,
    i: units._DensityUnit,
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
    data: "data._Data",
    f: units._UnitsType | units.Units,
) -> "data._Data":
    data = data.copy()

    if not isinstance(f, units.Units):
        f = units.Units(
            density=f[0],
            temperature=f[1],
            velocity=f[2],
            distance=f[3],
        )
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
    if len(data.grid_n.data) == 3:
        data.grid_n.data[2] = cd(data.grid_n.data[2])
        data.grid_v.data[2] = cd(data.grid_v.data[2])
    elif len(data.grid_n.data) == 2:
        data.grid_n.data[1] = cd(data.grid_n.data[1])
        data.grid_v.data[1] = cd(data.grid_v.data[1])
    elif len(data.grid_n.data) == 1:
        data.grid_n.data[0] = cd(data.grid_n.data[0])
        data.grid_v.data[0] = cd(data.grid_v.data[0])

    data.units = f
    return data