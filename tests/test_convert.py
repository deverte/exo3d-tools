import numpy as np
import pytest

import exo3d_tools as e3


def test_convert(make_data_3d):
    d1: e3.Data3Spherical = make_data_3d(
        Rplanet=2.0,
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr", "H1p.Tn"],
    )

    d1.units = e3.Units(
        density="cm-3",
        temperature="1e4 K",
        velocity="9.07 km s-1",
        distance="planet radius",
    )
    d2 = d1.convert(
        e3.Units(
            density="lg(cm-3)",
            temperature="K",
            velocity="km s-1",
            distance="Jupiter radius",
        ),
    )
    d3 = d2.convert(
        e3.Units(
            density="cm-3",
            temperature="1e4 K",
            velocity="9.07 km s-1",
            distance="km",
        ),
    )

    assert np.log10(d1.arrays["H1a.Pn"]) == pytest.approx(d2.arrays["H1a.Pn"])
    assert 1.0e4 * d1.arrays["H1p.Tn"] == pytest.approx(d2.arrays["H1p.Tn"])
    assert 9.07 * d1.arrays["H1p.Vr"] == pytest.approx(d2.arrays["H1p.Vr"])
    assert 1.0 / 2.0 * d1.grid_n.data[2] == pytest.approx(d2.grid_n.data[2])
    assert 1.0 / 2.0 * d1.grid_v.data[2] == pytest.approx(d2.grid_v.data[2])

    assert d1.arrays["H1a.Pn"] == pytest.approx(d3.arrays["H1a.Pn"])
    assert d1.arrays["H1p.Tn"] == pytest.approx(d3.arrays["H1p.Tn"])
    assert d1.arrays["H1p.Vr"] == pytest.approx(d3.arrays["H1p.Vr"])
    assert 7.1492e4 * d1.grid_n.data[2] == pytest.approx(d3.grid_n.data[2])
    assert 7.1492e4 * d1.grid_v.data[2] == pytest.approx(d3.grid_v.data[2])

    assert 10.0**d2.arrays["H1a.Pn"] == pytest.approx(d3.arrays["H1a.Pn"])
    assert 1.0e-4 * d2.arrays["H1p.Tn"] == pytest.approx(d3.arrays["H1p.Tn"])
    assert 1 / 9.07 * d2.arrays["H1p.Vr"] == pytest.approx(d3.arrays["H1p.Vr"])
    assert \
        2.0 * 7.1492e4 * d2.grid_n.data[2] == pytest.approx(d3.grid_n.data[2])
    assert \
        2.0 * 7.1492e4 * d2.grid_v.data[2] == pytest.approx(d3.grid_v.data[2])