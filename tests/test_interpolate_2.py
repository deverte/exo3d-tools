import pathlib

import numpy as np
import pytest

import exo3d_tools as e3


def test_interpolate_2(make_data_2d):
    d2: e3.Data2D = make_data_2d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    ds = d2["H1a.Pn"]
    dc = ds.to_cartesian()
    di = dc.interpolate(size=5, r_max=50)