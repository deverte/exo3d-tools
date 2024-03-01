import io
import pathlib
import zipfile

import pytest

import exo3d_tools as e3


def dat_1d_path(tmp_path: pathlib.Path) -> pathlib.Path:
    p = tmp_path / "scan.dat"
    return p


def dat_1d_zip(tmp_path: pathlib.Path) -> zipfile.Path:
    archive = tmp_path / "archive.zip"
    z = zipfile.ZipFile(archive, "w")
    p = zipfile.Path(z) / "scan.dat"
    return p


def dat_1d_fileio(tmp_path: pathlib.Path) -> io.FileIO:
    p = tmp_path / "scan.dat"
    f = io.FileIO(p, "w")
    return f


def dat_1d_bytesio(_) -> io.BytesIO:
    b = io.BytesIO()
    return b


def dat_1d_stringio(_) -> io.StringIO:
    s = io.StringIO()
    return s


file_generators = [
    (dat_1d_path),
    (dat_1d_zip),
    (dat_1d_fileio),
    (dat_1d_bytesio),
    (dat_1d_stringio),
]


@pytest.mark.parametrize("file_generator", file_generators)
def test_save_1d_dat(tmp_path, make_data_1d, file_generator):
    data: e3.Data1 = make_data_1d(
        Rmax=70.0,
        nR=4,
        nF=3,
        nTet=2,
        keys=["H1a.Pn", "H1p.Vr"],
    )

    file = file_generator(tmp_path)
    data.to_csv(file)

    if issubclass(type(file), io.FileIO):
        p = tmp_path / "scan.dat"
        file = io.FileIO(p, "r")

    file_data = e3.read_1d_csv(file)
    assert file_data == data