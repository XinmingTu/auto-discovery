"""Deterministic layered 14-point construction for minimizing_max_min_dist in 3D."""

from __future__ import annotations

import numpy as np

TWO_PI_OVER_THREE = 2.0 * np.pi / 3.0


def _triangle_layer(x_coord: float, radius: float, angle: float) -> np.ndarray:
    return np.array(
        [
            [x_coord, radius * np.cos(angle + k * TWO_PI_OVER_THREE), radius * np.sin(angle + k * TWO_PI_OVER_THREE)]
            for k in range(3)
        ],
        dtype=np.float64,
    )


def min_max_dist_dim3_14() -> np.ndarray:
    layers = [
        np.array([[0.0, 0.0, 0.0]], dtype=np.float64),
        _triangle_layer(-0.8164965809277264, 0.5773502691896257, 0.0),
        _triangle_layer(-0.32909696753644735, 1.00452541004774, -np.pi / 3.0),
        np.array([[1.1411678799150242, 0.0, 0.0]], dtype=np.float64),
        _triangle_layer(0.08816267789085401, 0.9961060898454107, 2.198566545727455),
        _triangle_layer(0.6376555162215236, 0.863988020523308, 1.2770183552029313),
    ]
    return np.vstack(layers)


if __name__ == "__main__":
    print(min_max_dist_dim3_14())
