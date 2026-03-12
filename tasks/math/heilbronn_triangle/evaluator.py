"""Evaluator imported from SkyDiscover for the Heilbronn triangle task."""

from __future__ import annotations

import itertools
import os
import sys
import time
from importlib import __import__

import numpy as np

BENCHMARK = 0.036529889880030156
TOL = 1e-6
NUM_POINTS = 11


def check_inside_triangle(points: np.ndarray, tol: float = TOL) -> None:
    for x_coord, y_coord in points:
        cond1 = y_coord >= -tol
        cond2 = np.sqrt(3.0) * x_coord <= np.sqrt(3.0) - y_coord + tol
        cond3 = y_coord <= np.sqrt(3.0) * x_coord + tol
        if not (cond1 and cond2 and cond3):
            raise ValueError(f"Point ({x_coord}, {y_coord}) is outside the triangle.")


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
            points = program.heilbronn_triangle11()
            end_time = time.time()
        finally:
            if program_dir in sys.path:
                sys.path.remove(program_dir)

        points = np.asarray(points, dtype=np.float64)
        if points.shape != (NUM_POINTS, 2):
            raise ValueError(f"Invalid shapes: points = {points.shape}, expected {(NUM_POINTS, 2)}")

        check_inside_triangle(points)

        triangle_vertices = np.array(
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [0.5, np.sqrt(3.0) / 2.0],
            ],
            dtype=np.float64,
        )
        normalization_area = triangle_area(
            triangle_vertices[0], triangle_vertices[1], triangle_vertices[2]
        )
        min_triangle_area = min(
            triangle_area(point_a, point_b, point_c)
            for point_a, point_b, point_c in itertools.combinations(points, 3)
        )
        min_area_normalized = float(min_triangle_area / normalization_area)
        return {
            "min_area_normalized": min_area_normalized,
            "combined_score": min_area_normalized / BENCHMARK,
            "eval_time": float(end_time - start_time),
        }
    except Exception as exc:
        return {"combined_score": 0.0, "error": str(exc)}
