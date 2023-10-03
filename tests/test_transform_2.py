import pytest

import exo3d_tools as e3


def test_transform_2(make_data_2d):
    d2: e3.Data2D = make_data_2d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    p1 = d2.grid
    c1 = p1.to_cartesian()
    p2 = c1.to_polar()
    c2 = p2.to_cartesian()
    p3 = c2.to_polar()
    c3 = p3.to_cartesian()

    assert p1.n[0] == pytest.approx(p2.n[0])
    assert p2.n[0] == pytest.approx(p3.n[0])
    assert c1.n[0] == pytest.approx(c2.n[0])
    assert c2.n[0] == pytest.approx(c3.n[0])