"""Physical units."""


from dataclasses import dataclass
import typing


_DensityUnit = typing.Literal["lg(cm-3)", "cm-3"]
_TemperatureUnit = typing.Literal["1e4 K", "K"]
_VelocityUnit = typing.Literal["9.07 km s-1", "km s-1"]
_DistanceUnit = typing.Literal["planet radius", "Jupiter radius", "km"]
_UnitsType = tuple[_DensityUnit, _TemperatureUnit, _VelocityUnit, _DistanceUnit]


@dataclass
class Units:
    """Physical units."""
    #: Density unit.
    density: _DensityUnit = "cm-3"
    #: Temperature unit.
    temperature: _TemperatureUnit = "K"
    #: Velocity unit.
    velocity: _VelocityUnit = "km s-1"
    #: Distance unit.
    distance: _DistanceUnit = "km"


EXO3D_UNITS = Units(
    density="cm-3",
    temperature="1e4 K",
    velocity="9.07 km s-1",
    distance="planet radius",
)
CVIEWER_UNITS = Units(
    density="lg(cm-3)",
    temperature="1e4 K",
    velocity="9.07 km s-1",
    distance="planet radius",
)
SCALED_UNITS = Units(
    density="cm-3",
    temperature="1e4 K",
    velocity="km s-1",
    distance="km",
)