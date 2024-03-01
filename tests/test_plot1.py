import matplotlib.pyplot as plt
import pytest

import exo3d_tools as e3


def test_plot_1(make_data_1d, tmp_path):
    data: e3.Data1 = make_data_1d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    ax = data["H1a.Pn"].plot()
    plt.savefig(tmp_path / "fig.png")