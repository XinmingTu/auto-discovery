"""Evaluator imported from SkyDiscover for rectangle circle packing."""

from __future__ import annotations

import os
import sys
import time
from importlib import __import__

import numpy as np

BENCHMARK = 2.3658321334167627
NUM_CIRCLES = 21
TOL = 1e-6


def minimum_circumscribing_rectangle(circles: np.ndarray) -> tuple[float, float]:
    min_x = np.min(circles[:, 0] - circles[:, 2])
    max_x = np.max(circles[:, 0] + circles[:, 2])
    min_y = np.min(circles[:, 1] - circles[:, 2])
    max_y = np.max(circles[:, 1] + circles[:, 2])
    return max_x - min_x, max_y - min_y


def validate_packing_radii(radii: np.ndarray) -> None:
    for index, radius in enumerate(radii):
        if radius < 0:
            raise ValueError(f"Circle {index} has negative radius {radius}")
        if np.isnan(radius):
            raise ValueError(f"Circle {index} has nan radius")


def validate_packing_overlap(circles: np.ndarray, tol: float = TOL) -> None:
    n_circles = len(circles)
    for left in range(n_circles):
        for right in range(left + 1, n_circles):
            distance = float(np.linalg.norm(circles[left, :2] - circles[right, :2]))
            if distance < circles[left, 2] + circles[right, 2] - tol:
                raise ValueError(
                    f"Circles {left} and {right} overlap: "
                    f"dist={distance}, r1+r2={circles[left, 2] + circles[right, 2]}"
                )


def validate_packing_inside_rect(circles: np.ndarray, tol: float = TOL) -> None:
    width, height = minimum_circumscribing_rectangle(circles)
    if width + height > 2.0 + tol:
        raise ValueError("Circles are not contained inside a rectangle of perimeter 4.")


def evaluate(program_path: str) -> dict[str, float | str]:
    try:
        abs_program_path = os.path.abspath(program_path)
        program_dir = os.path.dirname(abs_program_path)
        module_name = os.path.splitext(os.path.basename(program_path))[0]

        sys.path.insert(0, program_dir)
        try:
            program = __import__(module_name)
            start_time = time.time()
            circles = program.circle_packing21()
            end_time = time.time()
        finally:
            if program_dir in sys.path:
                sys.path.remove(program_dir)

        circles = np.asarray(circles, dtype=np.float64)
        if circles.shape != (NUM_CIRCLES, 3):
            raise ValueError(f"Invalid shapes: circles = {circles.shape}, expected {(NUM_CIRCLES, 3)}")

        validate_packing_radii(circles[:, 2])
        validate_packing_overlap(circles)
        validate_packing_inside_rect(circles)

        radii_sum = float(np.sum(circles[:, 2]))
        return {
            "radii_sum": radii_sum,
            "combined_score": radii_sum / BENCHMARK,
            "eval_time": float(end_time - start_time),
        }
    except Exception as exc:
        return {"combined_score": 0.0, "error": str(exc)}
