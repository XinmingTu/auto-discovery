"""Baseline rectangle circle packing seed imported from SkyDiscover."""

from __future__ import annotations

import numpy as np

N_CIRCLES = 21


def circle_packing21() -> np.ndarray:
    circles = np.zeros((N_CIRCLES, 3), dtype=np.float64)
    return circles


if __name__ == "__main__":
    circles = circle_packing21()
    print(f"radii_sum={np.sum(circles[:, 2]):.12f}")
