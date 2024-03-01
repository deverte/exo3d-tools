import pathlib
import zipfile

import typer

import exo3d_tools as e3


app = typer.Typer()


def read_d3(_input: pathlib.Path, zippath: str = ""):
    path = _input
    if len(zippath) > 0:
        path = zipfile.Path(_input) / zippath
    d3 = e3.read_3d_dat(path)
    return d3


def parse_units(
    units: str = "custom",
    density: str = "cm-3",
    temperature: str = "K",
    velocity: str = "km s-1",
    distance: str = "km",
):
    if units == "exo3d":
        return e3.EXO3D_UNITS
    elif units == "cviewer":
        return e3.CVIEWER_UNITS
    elif units == "scaled":
        return e3.SCALED_UNITS
    return e3.Units(
        density=density,
        temperature=temperature,
        velocity=velocity,
        distance=distance,
    )


@app.command()
def keys(
    _input: pathlib.Path,
    zippath: str = "",
):
    d3 = read_d3(_input, zippath)

    print("Keys:")
    print("\n".join(d3.keys()))


@app.command()
def to_1d_csv(
    _input: pathlib.Path,
    output: pathlib.Path,
    zippath: str = "",
    phi: float = 0,
    theta: float = 0,
    units: str = "custom",
    density: str = "cm-3",
    temperature: str = "K",
    velocity: str = "km s-1",
    distance: str = "km",
):
    d3 = read_d3(_input, zippath)
    d3 = d3.convert(
        parse_units(units, density, temperature, velocity, distance)
    )

    d1 = d3.to_1d(theta=theta, phi=phi)
    d1.to_csv(output)


@app.command()
def to_3d_csv(
    _input: pathlib.Path,
    output: pathlib.Path,
    key: str,
    zippath: str = "",
    units: str = "custom",
    density: str = "cm-3",
    temperature: str = "K",
    velocity: str = "km s-1",
    distance: str = "km",
    coordinate_system: str = "cartesian",
):
    d3 = read_d3(_input, zippath)
    d3 = d3.convert(
        parse_units(units, density, temperature, velocity, distance)
    )

    if coordinate_system == "cartesian":
        d3.to_csv_cartesian(output)
    elif coordinate_system == "spherical":
        d3.to_csv_spherical(output)


if __name__ == "__main__":
    app()