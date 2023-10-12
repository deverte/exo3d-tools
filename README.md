# exo3d_tools

exo3d tools (read and save data, projections, interpolation, 1D, 2D plotting)
library for exo3d (exoplanets atmospheres numerical simulation code).

## Installation


```sh
# Using PIP
# Install using PyPI package with Matplotlib
pip3 install --index-url https://gitea.zarux.ru/api/packages/astro/pypi/simple exo3d-tools[matplotlib]
# Install using PyPI package without extras
pip3 install --index-url https://gitea.zarux.ru/api/packages/astro/pypi/simple exo3d-tools
# Install using git url with Matplotlib
pip3 install git+https://gitea.zarux.ru/astro/exo3d-tools#egg=exo3d-tools[matplotlib]
# Install using git url without extras
pip3 install git+https://gitea.zarux.ru/astro/exo3d-tools

# Using poetry
# Add source
poetry source add --priority=explicit astro https://gitea.zarux.ru/api/packages/astro/pypi/simple
# Install with Matplotlib
poetry add --source=astro exo3d-tools[matplotlib]
# Install without extras
poetry add --source=astro exo3d-tools
```

## Usage

In this documentation will be assumed that `exo3d_tools` is imported as `e3`.

### Data classes

Main data classes are: `e3.Data1D`, `e3.Data2D` and `e3.Data3D`.

```python
import numpy as np
import exo3d_tools as e3

Rmax = 70.0
nR = 180
nF = 97
nTet = 28
keys = ["H1a.Pn", "H1p.Vr"]

rng = np.random.default_rng(seed=42)
r_v = np.linspace(1.0, 0.95 * Rmax, nR + 1)
phi_v = np.linspace(0.0, 2 * np.pi, nF + 1)
theta_v = np.linspace(-np.pi / 2, np.pi / 2, nTet + 2)
r_n = np.linspace(1.0 + 0.001 * Rmax, Rmax, nR + 1)
phi_n = np.linspace(0.0, 2 * np.pi, nF + 1)
theta_n = np.linspace(-np.pi / 2, np.pi / 2, nTet + 1)

data = e3.Data3D(
    keys=keys,
    params={
        "Rmax": f"{Rmax}",
        "nR": f"{nR}",
        "nF": f"{nF}",
        "nTet": f"{nTet}",
    },
    arrays={
        key: rng.random((nTet + 2, nF + 1, nR + 1))
        if ".Vr" in key or ".Vt" in key or ".Vf" in key
        else rng.random((nTet + 1, nF + 1, nR + 1)) for key in keys
    },
    grid=e3.Grid3D(
        v=np.meshgrid(theta_v, phi_v, r_v),
        n=np.meshgrid(theta_n, phi_n, r_n),
    ),
)
```

### Read data

`e3.Data3D` or `e3.Data1D` can be loaded from `pathlib.Path`, `zipfile.Path`,
`io.FileIO`, `io.BytesIO` or `io.StringIO`.

```python
import zipfile
import exo3d_tools as e3

file = zipfile.Path("archive.zip") / "Result.dat"
data = e3.from_3d_dat(file)
```

### Units conversion

```python
d3 = e3.from_3d_dat(file_3d)

d3.units # Units(density="cm-3", temperature="1e4 K",
         # velocity="9.07 km s-1", distance="planet radius")
d3s = d_e3.convert(e3.Units(temperature="K", velocity="km s-1", distance="km"))
d3s.units # Units(density="cm-3", temperature="1e4 K",
          # velocity="km s-1", distance="km")


d1 = e3.from_1d_dat(file_1d) # without planet radius
d1.params["Rplanet"] = str(2.0)
d1.units # Units(density="lg(cm-3)", temperature="1e4 K",
         # velocity="9.07 km s-1", distance="planet radius")
```

For convenience, there are units presets:

- `e3.EXO3D_UNITS == e3.Units("cm-3", "1e4 K", "9.07 km s-1", "planet radius")`
- `e3.CVIEWER_UNITS == e3.Units("lg(cm-3)", "1e4 K", "9.07 km s-1", "planet radius")`
- `e3.SCALED_UNITS == e3.Units("cm-3", "K", "km s-1", "km")`

### Projection

```python
import exo3d_tools as e3

d3 = e3.Data3D(...)

d2 = d3.to_2d(theta=0)
d1 = d3.to_1d(theta=0, phi=0)
d1 = d2.to_1d(phi=0)
```

### Interpolation

```python
import exo3d_tools as e3

d3 = e3.Data3D(...)
```

### Graphics

Graphics available for `e3.Data2D` and `e3.Data1D` data using Matplotlib
library.

Can be used directly.

```python
import exo3d_tools as e3

data = e3.Data2D(...)

key = "H1a.Pn"
data[key].to_cartesian().interpolate(size=250, r_max=30.0).mirror("x").plot()
```

Or using Matplotlib axis.

```python
import matplotlib.pyplot as plt
import exo3d_tools as e3

data = e3.Data2D(...)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("Title")
ax.set_xlabel("X")
ax.set_ylabel("Y")
data[key].plot(ax=ax)
ax.show()
```

### Save data

Data can be saved for `e3.Data3D` or `e3.Data1D` into the following types:
`pathlib.Path`, `zipfile.Path`, `io.FileIO`, `io.BytesIO` or `io.StringIO`.

```python
import zipfile
import exo3d_tools as e3

data = e3.Data3D(...)

z = zipfile.ZipFile("archive.zip", "w")
file = zipfile.Path(z) / "Result.dat"

data.to_dat(file)
```

## License

Author: [Artem Shepelin](mailto:deverte@ya.ru)
License: [GPL v3](./LICENSE)