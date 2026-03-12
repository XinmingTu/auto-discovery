"""Evaluator imported from SkyDiscover for minimizing_max_min_dist in 3D."""

from __future__ import annotations

import os
import sys
import time
from importlib import __import__

import numpy as np
import scipy as sp

NUM_POINTS = 14
DIMENSION = 3
BENCHMARK = 1.0 / 4.165849767


def evaluate(program_path: str) -> dict[str, float | str]:
    try:
        abs_program_path = os.path.abspath(program_path)
        program_dir = os.path.dirname(abs_program_path)
        module_name = os.path.splitext(os.path.basename(program_path))[0]

        sys.path.insert(0, program_dir)
        try:
            program = __import__(module_name)
            start_time = time.time()
            points = program.min_max_dist_dim3_14()
            end_time = time.time()
        finally:
            if program_dir in sys.path:
                sys.path.remove(program_dir)

        points = np.asarray(points, dtype=np.float64)
        if points.shape != (NUM_POINTS, DIMENSION):
            raise ValueError(f"Invalid shapes: points = {points.shape}, expected {(NUM_POINTS, DIMENSION)}")

        pairwise_distances = sp.spatial.distance.pdist(points)
        min_distance = float(np.min(pairwise_distances))
        max_distance = float(np.max(pairwise_distances))
        min_max_ratio = (min_distance / max_distance) ** 2 if max_distance > 0 else 0.0
        return {
            "min_max_ratio": float(min_max_ratio),
            "combined_score": float(min_max_ratio / BENCHMARK),
            "eval_time": float(end_time - start_time),
        }
    except Exception as exc:
        return {"combined_score": 0.0, "error": str(exc)}
