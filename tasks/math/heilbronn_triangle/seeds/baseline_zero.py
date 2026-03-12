"""Baseline seed snapshot for the heilbronn_triangle task."""

from __future__ import annotations

import numpy as np

N_POINTS = 11


def heilbronn_triangle11() -> np.ndarray:
    points = np.zeros((N_POINTS, 2), dtype=np.float64)
    return points
