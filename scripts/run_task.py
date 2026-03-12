from __future__ import annotations

import argparse
import importlib.util
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _tasks import TaskConfig, git_commit_short, load_task_config, relative_to_repo

RESULTS_HEADER = (
    "timestamp\tcommit\ttask\tobjective\tprimary_metric\tscore\tstatus\twall_seconds\tsolution\tnotes\n"
)


def _load_module(module_name: str, module_path: Path, extra_path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not import module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(extra_path))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def _format_score(value: float) -> str:
    if math.isfinite(value):
        return f"{value:.12g}"
    return "nan"


def _append_result(
    task: TaskConfig,
    solution_path: Path,
    score: float,
    status: str,
    wall_seconds: float,
    notes: str,
) -> None:
    results_path = task.task_dir / "results.tsv"
    if not results_path.exists():
        results_path.write_text(RESULTS_HEADER)

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    row = [
        timestamp,
        git_commit_short(),
        task.task_id,
        task.objective,
        task.primary_metric,
        _format_score(score),
        status,
        f"{wall_seconds:.3f}",
        relative_to_repo(solution_path),
        notes.replace("\t", " ").strip(),
    ]
    with results_path.open("a") as handle:
        handle.write("\t".join(row) + "\n")


def _run_evaluation(task: TaskConfig, solution_path: Path) -> tuple[dict[str, Any], float, str]:
    evaluator_path = task.task_dir / task.evaluator_file
    evaluator = _load_module(f"task_eval_{task.name}", evaluator_path, task.task_dir)
    if not hasattr(evaluator, "evaluate"):
        raise AttributeError(f"{evaluator_path} does not define evaluate(program_path)")

    start = time.perf_counter()
    metrics = evaluator.evaluate(str(solution_path))
    wall_seconds = time.perf_counter() - start
    if not isinstance(metrics, dict):
        raise TypeError(f"{evaluator_path} returned {type(metrics)!r}; expected dict")
    return metrics, wall_seconds, "ok"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one task evaluator against a solution file.")
    parser.add_argument("task", help="Task id like math/circle_packing or a unique leaf task name.")
    parser.add_argument("--solution", help="Override the solution file path relative to the task directory.")
    parser.add_argument("--notes", default="", help="Short note to append to results.tsv.")
    parser.add_argument("--no-log", action="store_true", help="Skip appending to results.tsv.")
    args = parser.parse_args()

    task = load_task_config(args.task)
    solution_rel = args.solution or task.entry_file
    solution_path = (task.task_dir / solution_rel).resolve()

    try:
        metrics, wall_seconds, status = _run_evaluation(task, solution_path)
        raw_score = metrics.get(task.primary_metric)
        if not isinstance(raw_score, (int, float)):
            raise TypeError(
                f"Primary metric '{task.primary_metric}' missing or non-numeric in evaluator output"
            )
        score = float(raw_score)
    except Exception as exc:
        metrics = {"error": str(exc)}
        wall_seconds = 0.0
        status = "error"
        score = math.nan

    if not args.no_log:
        _append_result(task, solution_path, score, status, wall_seconds, args.notes)

    print(f"task: {task.task_id}")
    print(f"objective: {task.objective}")
    print(f"primary_metric: {task.primary_metric}")
    print(f"score: {_format_score(score)}")
    print(f"status: {status}")
    print(f"wall_seconds: {wall_seconds:.3f}")
    for key in task.display_metrics:
        value = metrics.get(key)
        if isinstance(value, (int, float)):
            print(f"{key}: {_format_score(float(value))}")
    if "error" in metrics:
        print(f"error: {metrics['error']}")


if __name__ == "__main__":
    main()
