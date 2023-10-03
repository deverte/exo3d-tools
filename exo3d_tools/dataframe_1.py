"""Dataframes."""


import numpy as np
import pandas as pd


def _dataframe_1(data: "exo3d_tools.Data1D") -> pd.DataFrame:
    r = data.grid.n
    theta = data.grid.theta
    phi = data.grid.phi
    x = r * np.sin(theta + np.pi / 2) * np.cos(phi)
    y = r * np.sin(theta + np.pi / 2) * np.sin(phi)
    z = r * np.cos(theta + np.pi / 2)

    df = pd.DataFrame()
    df["x"] = x
    df["Y"] = y
    df["Z"] = z
    for key in data.arrays.keys():
        df[key] = data.arrays[key]

    return df