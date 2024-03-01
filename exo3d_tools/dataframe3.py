"""Dataframes."""


import exo3d_tools.data3_cartesian as data3_cartesian

import numpy as np
import pandas as pd


def _dataframe_3_cartesian(
    data: "data3_cartesian.Data3Cartesian",
) -> pd.DataFrame:
    x = np.ravel(data.grid.n[2])
    y = np.ravel(data.grid.n[1])
    z = np.ravel(data.grid.n[0])

    df = pd.DataFrame()
    df["x"] = x
    df["y"] = y
    df["z"] = z
    df[data.key] = np.ravel(data.array)

    return df