import pathlib
import warnings

import matplotlib.pyplot as plt
import pytest

import exo3d_tools as e3


@pytest.mark.filterwarnings("ignore:plot")
def test_plot_2(make_data_2d, tmp_path):
    data: e3.Data2Polar = make_data_2d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    data["H1a.Pn"].plot()
    plt.savefig(tmp_path / "polar.png")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data["H1a.Pn"].to_cartesian().plot()
    plt.savefig(tmp_path / "cartesian.png")
    data["H1a.Pn"].to_cartesian().to_polar().plot()
    plt.savefig(tmp_path / "polar2.png")