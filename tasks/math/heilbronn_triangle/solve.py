"""Deterministic 11-point construction for the Heilbronn triangle task."""

from __future__ import annotations

import numpy as np

_POINTS = np.array(
    [
        [0.1062310826141214, 0.07107669277538832],
        [0.8937689173858786, 0.07107669277538832],
        [0.27745297791550644, 0.0],
        [0.7225470220844936, 0.0],
        [0.14782557294066753, 0.25604140299121514],
        [0.8521744270593324, 0.25604140299121514],
        [0.40933520785733885, 0.4392918971067322],
        [0.5906647921426611, 0.4392918971067322],
        [0.4279845295533237, 0.7412909500398204],
        [0.5720154704466762, 0.7412909500398204],
        [0.5, 0.21112642591903782],
    ],
    dtype=np.float64,
)


def heilbronn_triangle11() -> np.ndarray:
    return _POINTS.copy()


if __name__ == "__main__":
    print(heilbronn_triangle11())
