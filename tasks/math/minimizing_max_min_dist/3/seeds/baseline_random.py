"""Baseline seed snapshot for minimizing_max_min_dist in 3D."""

from __future__ import annotations

import numpy as np

N_POINTS = 14
DIMENSION = 3


def min_max_dist_dim3_14() -> np.ndarray:
    np.random.seed(42)
    return np.random.randn(N_POINTS, DIMENSION)
