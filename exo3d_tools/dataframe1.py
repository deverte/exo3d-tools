"""Dataframes."""


import exo3d_tools.data1 as data1

import numpy as np
import pandas as pd


def _dataframe_1(data: "data1.Data1") -> pd.DataFrame:
    r = data.grid.data
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