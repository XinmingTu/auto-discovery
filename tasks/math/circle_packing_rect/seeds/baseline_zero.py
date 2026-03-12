"""Baseline seed snapshot for the circle_packing_rect task."""

from __future__ import annotations

import numpy as np

N_CIRCLES = 21


def circle_packing21() -> np.ndarray:
    circles = np.zeros((N_CIRCLES, 3), dtype=np.float64)
    return circles
