"""Evaluator imported from SkyDiscover for Heilbronn convex with 13 points."""

from __future__ import annotations

import itertools
import os
import sys
import time
from importlib import __import__

import numpy as np
from scipy.spatial import ConvexHull

BENCHMARK = 0.030936889034895654
NUM_POINTS = 13


def triangle_area(point_a: np.ndarray, point_b: np.ndarray, point_c: np.ndarray) -> float:
    return abs(
        point_a[0] * (point_b[1] - point_c[1])
        + point_b[0] * (point_c[1] - point_a[1])
        + point_c[0] * (point_a[1] - point_b[1])
    ) / 2.0


def evaluate(program_path: str) -> dict[str, float | str]:
    try:
        abs_program_path = os.path.abspath(program_path)
        program_dir = os.path.dirname(abs_program_path)
        module_name = os.path.splitext(os.path.basename(program_path))[0]

        sys.path.insert(0, program_dir)
        try:
            program = __import__(module_name)
            start_time = time.time()
            points = program.heilbronn_convex13()
            end_time = time.time()
        finally:
            if program_dir in sys.path:
                sys.path.remove(program_dir)

        points = np.asarray(points, dtype=np.float64)
        if points.shape != (NUM_POINTS, 2):
            raise ValueError(f"Invalid shapes: points = {points.shape}, expected {(NUM_POINTS, 2)}")

        min_triangle_area = min(
            triangle_area(point_a, point_b, point_c)
            for point_a, point_b, point_c in itertools.combinations(points, 3)
        )
        convex_hull_area = float(ConvexHull(points).volume)
        min_area_normalized = float(min_triangle_area / convex_hull_area)
        return {
            "min_area_normalized": min_area_normalized,
            "combined_score": float(min_area_normalized / BENCHMARK),
            "eval_time": float(end_time - start_time),
        }
    except Exception as exc:
        return {"combined_score": 0.0, "error": str(exc)}
