import io
import pathlib
import zipfile

import numpy as np
import pytest

import exo3d_tools as e3


def dat_3d_path(tmp_path: pathlib.Path, text_data_3d: str) -> pathlib.Path:
    p = tmp_path / "Result.dat"
    p.write_text(text_data_3d, encoding="utf-8")
    return p


def dat_3d_zip(tmp_path: pathlib.Path, text_data_3d: str) -> zipfile.Path:
    archive = tmp_path / "archive.zip"
    zipfile.ZipFile(archive, "w").writestr("Result.dat", text_data_3d)
    p = zipfile.Path(archive) / "Result.dat"
    return p


def dat_3d_fileio(tmp_path: pathlib.Path, text_data_3d: str) -> io.FileIO:
    p = tmp_path / "Result.dat"
    p.write_text(text_data_3d, encoding="utf-8")
    f = io.FileIO(p)
    return f


def dat_3d_bytesio(_, text_data_3d: str) -> io.BytesIO:
    b = io.BytesIO(str.encode(text_data_3d))
    return b


def dat_3d_stringio(_, text_data_3d: str) -> io.StringIO:
    s = io.StringIO(text_data_3d)
    return s


file_generators = [
    (dat_3d_path),
    (dat_3d_zip),
    (dat_3d_fileio),
    (dat_3d_bytesio),
    (dat_3d_stringio),
]


@pytest.mark.parametrize("file_generator", file_generators)
def test_read_3d_dat(tmp_path, text_data_3d, file_generator):
    file = file_generator(tmp_path, text_data_3d)
    data = e3.read_3d_dat(file)

    assert list(data.keys()) == ["H1a.Pn", "H1p.Vr"]

    nR = 4
    nF = 3
    nTet = 2
    Rmax = 70.0
    assert len(data.params) == 4
    assert data.params["Rmax"] == str(Rmax)
    assert int(data.params["nR"]) == nR
    assert int(data.params["nF"]) == nF
    assert int(data.params["nTet"]) == nTet

    theta_v = np.linspace(-np.pi / 2.0, np.pi / 2.0, nTet + 2)
    theta_n = np.linspace(-np.pi / 2.0, np.pi / 2.0, nTet + 1)
    phi_v = np.linspace(0.0, 2.0 * np.pi, nF + 1)
    phi_n = np.linspace(0.0, 2.0 * np.pi, nF + 1)
    r_v = np.linspace(1.0, 0.95 * Rmax, nR + 1)
    r_n = np.linspace(1.0 + 0.001 * Rmax, Rmax, nR + 1)
    assert (data.grid_v.data[0] == np.meshgrid(theta_v, phi_v, r_v)[0]).all()
    assert (data.grid_v.data[1] == np.meshgrid(theta_v, phi_v, r_v)[1]).all()
    assert (data.grid_v.data[2] == np.meshgrid(theta_v, phi_v, r_v)[2]).all()
    assert (data.grid_n.data[0] == np.meshgrid(theta_n, phi_n, r_n)[0]).all()
    assert (data.grid_n.data[1] == np.meshgrid(theta_n, phi_n, r_n)[1]).all()
    assert (data.grid_n.data[2] == np.meshgrid(theta_n, phi_n, r_n)[2]).all()