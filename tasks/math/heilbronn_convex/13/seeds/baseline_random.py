"""Baseline seed snapshot for Heilbronn convex with 13 points."""

from __future__ import annotations

import numpy as np

N_POINTS = 13


def heilbronn_convex13() -> np.ndarray:
    rng = np.random.default_rng(seed=42)
    return rng.random((N_POINTS, 2))
