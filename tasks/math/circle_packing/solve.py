"""Constructor-based circle packing baseline for 26 circles."""

from __future__ import annotations

import numpy as np

N_CIRCLES = 26


def construct_packing() -> tuple[np.ndarray, np.ndarray, float]:
    centers = np.zeros((N_CIRCLES, 2), dtype=np.float64)

    centers[0] = [0.5, 0.5]

    for index in range(8):
        angle = 2.0 * np.pi * index / 8.0
        centers[index + 1] = [0.5 + 0.3 * np.cos(angle), 0.5 + 0.3 * np.sin(angle)]

    for index in range(16):
        angle = 2.0 * np.pi * index / 16.0
        centers[index + 9] = [0.5 + 0.7 * np.cos(angle), 0.5 + 0.7 * np.sin(angle)]

    centers = np.clip(centers, 0.01, 0.99)
    radii = compute_max_radii(centers)
    sum_radii = float(np.sum(radii))
    return centers, radii, sum_radii


def compute_max_radii(centers: np.ndarray) -> np.ndarray:
    n_circles = centers.shape[0]
    radii = np.ones(n_circles, dtype=np.float64)

    for index, (x_coord, y_coord) in enumerate(centers):
        radii[index] = min(x_coord, y_coord, 1.0 - x_coord, 1.0 - y_coord)

    for left in range(n_circles):
        for right in range(left + 1, n_circles):
            distance = float(np.linalg.norm(centers[left] - centers[right]))
            total_radius = radii[left] + radii[right]
            if total_radius > distance:
                scale = distance / total_radius
                radii[left] *= scale
                radii[right] *= scale

    return radii


def run_packing() -> tuple[np.ndarray, np.ndarray, float]:
    return construct_packing()


if __name__ == "__main__":
    _, _, sum_radii = run_packing()
    print(f"sum_radii={sum_radii:.12f}")
