import io
import pathlib
import zipfile

import numpy as np
import pytest

import exo3d_tools as e3


def dat_1d_path(tmp_path: pathlib.Path, text_data_3d: str) -> pathlib.Path:
    p = tmp_path / "scan.dat"
    p.write_text(text_data_3d, encoding="utf-8")
    return p


def dat_1d_zip(tmp_path: pathlib.Path, text_data_3d: str) -> zipfile.Path:
    archive = tmp_path / "archive.zip"
    zipfile.ZipFile(archive, "w").writestr("scan.dat", text_data_3d)
    p = zipfile.Path(archive) / "scan.dat"
    return p


def dat_1d_fileio(tmp_path: pathlib.Path, text_data_3d: str) -> io.FileIO:
    p = tmp_path / "scan.dat"
    p.write_text(text_data_3d, encoding="utf-8")
    f = io.FileIO(p)
    return f


def dat_1d_bytesio(_, text_data_3d: str) -> io.BytesIO:
    b = io.BytesIO(str.encode(text_data_3d))
    return b


def dat_1d_stringio(_, text_data_3d: str) -> io.StringIO:
    s = io.StringIO(text_data_3d)
    return s


file_generators = [
    (dat_1d_path),
    (dat_1d_zip),
    (dat_1d_fileio),
    (dat_1d_bytesio),
    (dat_1d_stringio),
]


@pytest.mark.parametrize("file_generator", file_generators)
def test_read_1d_csv(tmp_path, text_data_1d, file_generator):
    file = file_generator(tmp_path, text_data_1d)
    data = e3.read_1d_csv(file)

    assert list(data.keys()) == ["H1a.Pn", "H1p.Vr"]

    nR = 4
    Rmax = 68.25
    assert len(data.params) == 2
    assert data.params["Rmax"] == str(Rmax)
    assert int(data.params["nR"]) == nR

    r = np.array([-68.2500, -51.4463, -34.6425, -17.8388, -1.0350, 1.0350, 17.8388, 34.6425, 51.4463, 68.2500])
    assert (data.grid.data == r).all()