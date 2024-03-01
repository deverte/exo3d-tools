import io
import pathlib
import zipfile

import pytest

import exo3d_tools as e3


def dat_3d_path(tmp_path: pathlib.Path) -> pathlib.Path:
    p = tmp_path / "Result.dat"
    return p


def dat_3d_zip(tmp_path: pathlib.Path) -> zipfile.Path:
    archive = tmp_path / "archive.zip"
    z = zipfile.ZipFile(archive, "w")
    p = zipfile.Path(z) / "Result.dat"
    return p


def dat_3d_fileio(tmp_path: pathlib.Path) -> io.FileIO:
    p = tmp_path / "Result.dat"
    f = io.FileIO(p, "w")
    return f


def dat_3d_bytesio(_) -> io.BytesIO:
    b = io.BytesIO()
    return b


def dat_3d_stringio(_) -> io.StringIO:
    s = io.StringIO()
    return s


file_generators = [
    (dat_3d_path),
    (dat_3d_zip),
    (dat_3d_fileio),
    (dat_3d_bytesio),
    (dat_3d_stringio),
]


@pytest.mark.parametrize("file_generator", file_generators)
def test_save_3d_dat(tmp_path, make_data_3d, file_generator):
    data: e3.Data3Spherical = make_data_3d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    file = file_generator(tmp_path)
    data.to_dat(file)

    if issubclass(type(file), io.FileIO):
        p = tmp_path / "Result.dat"
        file = io.FileIO(p, "r")

    file_data = e3.read_3d_dat(file)
    assert file_data.params == data.params
    assert file_data.keys() == data.keys()