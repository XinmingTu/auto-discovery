"""Baseline imported from SkyDiscover for minimizing_max_min_dist in 2D."""

from __future__ import annotations

import numpy as np

N_POINTS = 16
DIMENSION = 2


def min_max_dist_dim2_16() -> np.ndarray:
    np.random.seed(42)
    return np.random.randn(N_POINTS, DIMENSION)


if __name__ == "__main__":
    print(min_max_dist_dim2_16())
