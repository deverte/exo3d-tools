import pytest

import exo3d_tools as e3


def test_transform_3(make_data_3d):
    d3: e3.Data3Spherical = make_data_3d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    s1 = d3.grid_n
    c1 = s1.to_cartesian()
    s2 = c1.to_spherical()
    c2 = s2.to_cartesian()
    s3 = c2.to_spherical()
    c3 = s3.to_cartesian()

    assert s1.data[0] == pytest.approx(s2.data[0])
    assert s2.data[0] == pytest.approx(s3.data[0])
    assert c1.data[0] == pytest.approx(c2.data[0])
    assert c2.data[0] == pytest.approx(c3.data[0])