import pytest

import exo3d_tools as e3


def test_transform_3(make_data_3d):
    d3: e3.Data3D = make_data_3d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    s1 = d3.grid
    c1 = s1.to_cartesian()
    s2 = c1.to_spherical()
    c2 = s2.to_cartesian()
    s3 = c2.to_spherical()
    c3 = s3.to_cartesian()

    assert s1.v[0] == pytest.approx(s2.v[0])
    assert s1.n[0] == pytest.approx(s2.n[0])
    assert s2.v[0] == pytest.approx(s3.v[0])
    assert s2.n[0] == pytest.approx(s3.n[0])
    assert c1.v[0] == pytest.approx(c2.v[0])
    assert c1.n[0] == pytest.approx(c2.n[0])
    assert c2.v[0] == pytest.approx(c3.v[0])
    assert c2.n[0] == pytest.approx(c3.n[0])