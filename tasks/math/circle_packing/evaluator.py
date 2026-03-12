"""Circle packing evaluator imported from SkyDiscover and trimmed for local runs."""

from __future__ import annotations

import pickle
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

import numpy as np

EXPECTED_CIRCLES = 26
TARGET_SUM = 2.635


def validate_packing(centers: np.ndarray, radii: np.ndarray) -> bool:
    if centers.shape != (EXPECTED_CIRCLES, 2) or radii.shape != (EXPECTED_CIRCLES,):
        return False
    if np.isnan(centers).any() or np.isnan(radii).any():
        return False
    if np.any(radii < 0):
        return False

    for (x, y), radius in zip(centers, radii):
        if x - radius < -1e-6 or x + radius > 1.0 + 1e-6:
            return False
        if y - radius < -1e-6 or y + radius > 1.0 + 1e-6:
            return False

    for i in range(EXPECTED_CIRCLES):
        for j in range(i + 1, EXPECTED_CIRCLES):
            dist = float(np.linalg.norm(centers[i] - centers[j]))
            if dist < radii[i] + radii[j] - 1e-6:
                return False

    return True


def run_with_timeout(program_path: str, timeout_seconds: int = 600) -> tuple[np.ndarray, np.ndarray, float]:
    candidate_path = Path(program_path).resolve()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        driver_path = tmpdir_path / "driver.py"
        results_path = tmpdir_path / "results.pkl"

        driver_path.write_text(
            f"""
import importlib.util
import pickle
import traceback
from pathlib import Path

program_path = Path({str(candidate_path)!r})
results_path = Path({str(results_path)!r})

try:
    spec = importlib.util.spec_from_file_location("candidate_program", program_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    centers, radii, reported_sum = module.run_packing()
    with results_path.open("wb") as handle:
        pickle.dump({{"centers": centers, "radii": radii, "reported_sum": reported_sum}}, handle)
except Exception:
    with results_path.open("wb") as handle:
        pickle.dump({{"error": traceback.format_exc()}}, handle)
"""
        )

        subprocess.run(
            [sys.executable, str(driver_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )

        if not results_path.exists():
            raise RuntimeError("Evaluator subprocess produced no results file")

        with results_path.open("rb") as handle:
            payload = pickle.load(handle)

    if "error" in payload:
        raise RuntimeError(payload["error"])

    centers = np.asarray(payload["centers"], dtype=np.float64)
    radii = np.asarray(payload["radii"], dtype=np.float64)
    reported_sum = float(payload["reported_sum"])
    return centers, radii, reported_sum


def evaluate(program_path: str) -> dict[str, float]:
    try:
        centers, radii, reported_sum = run_with_timeout(program_path)
        valid = validate_packing(centers, radii)
        sum_radii = float(np.sum(radii)) if valid else 0.0
        target_ratio = (sum_radii / TARGET_SUM) if valid else 0.0
        validity = 1.0 if valid else 0.0
        combined_score = target_ratio * validity
        return {
            "sum_radii": sum_radii,
            "reported_sum": reported_sum,
            "target_ratio": target_ratio,
            "validity": validity,
            "combined_score": combined_score,
        }
    except Exception:
        traceback.print_exc()
        return {
            "sum_radii": 0.0,
            "reported_sum": 0.0,
            "target_ratio": 0.0,
            "validity": 0.0,
            "combined_score": 0.0,
        }
