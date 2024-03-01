"""3D data."""


from dataclasses import dataclass

import numpy as np


@dataclass
class _Grid:
    """Grid."""
    data: list | np.ndarray