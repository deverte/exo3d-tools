import pathlib

import numpy as np
import pytest

import exo3d_tools as e3


def test_projection_3_1(make_data_3d):
    Rmax = 70.0
    nR = 4
    d3: e3.Data3D = make_data_3d(
        Rmax=Rmax,
        nR=nR,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    d1 = d3.to_1d()

    r_n = np.linspace(1.0 + 0.001 * Rmax, Rmax, nR + 1)
    assert (d1.grid.n == np.concatenate((-np.flip(r_n), r_n))).all()
    array_H1aPn = np.array([
        0.4695558112758079,
        0.3704597060348689,
        0.32582535813815194,
        0.96750973243421,
        0.7447621559078171,
        0.7580877400853738,
        0.35452596812986836,
        0.9706980243949033,
        0.8931211213221977,
        0.7783834970737619,
    ])
    assert (d1.arrays["H1a.Pn"] == array_H1aPn).all()
    array_H1pVr = np.array([
        0.1767727829392317,
        0.579219568941896,
        0.3059566241506525,
        0.20236336479523032,
        0.45577628983361107,
        0.908580690707607,
        0.6997071338107496,
        0.2658699614595196,
        0.9691763773477239,
        0.7787509039657946,
    ])
    assert (d1.arrays["H1p.Vr"] == array_H1pVr).all()