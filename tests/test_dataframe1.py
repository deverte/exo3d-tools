import pytest

import exo3d_tools as e3


def test_dataframe_1(make_data_1d):
    data: e3.Data1 = make_data_1d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    df = data.to_dataframe()

    assert df["x"][0] == -70.0