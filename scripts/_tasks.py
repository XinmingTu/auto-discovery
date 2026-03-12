from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = REPO_ROOT / "tasks"


@dataclass(frozen=True)
class TaskConfig:
    task_id: str
    task_dir: Path
    name: str
    domain: str
    objective: str
    entry_file: str
    evaluator_file: str
    primary_metric: str
    display_metrics: tuple[str, ...]
    allowed_edit_paths: tuple[str, ...]
    timeout_sec: int | None
    description: str
    source: str


def _task_config_paths() -> list[Path]:
    return sorted(TASKS_ROOT.glob("**/task.json"))


def _task_id(task_dir: Path) -> str:
    return task_dir.relative_to(TASKS_ROOT).as_posix()


def resolve_task_dir(task_ref: str) -> Path:
    raw = Path(task_ref)
    direct = TASKS_ROOT / raw
    if (direct / "task.json").exists():
        return direct

    matches = []
    for config_path in _task_config_paths():
        task_dir = config_path.parent
        if task_ref in {_task_id(task_dir), task_dir.name}:
            matches.append(task_dir)

    if not matches:
        raise FileNotFoundError(f"No task found for '{task_ref}'")
    if len(matches) > 1:
        options = ", ".join(sorted(_task_id(path) for path in matches))
        raise ValueError(f"Ambiguous task '{task_ref}'. Use one of: {options}")
    return matches[0]


def load_task_config(task_ref: str) -> TaskConfig:
    task_dir = resolve_task_dir(task_ref)
    payload = json.loads((task_dir / "task.json").read_text())
    objective = payload["objective"]
    if objective not in {"maximize", "minimize"}:
        raise ValueError(f"Unsupported objective '{objective}' in {task_dir / 'task.json'}")

    return TaskConfig(
        task_id=_task_id(task_dir),
        task_dir=task_dir,
        name=payload["name"],
        domain=payload["domain"],
        objective=objective,
        entry_file=payload["entry_file"],
        evaluator_file=payload["evaluator_file"],
        primary_metric=payload["primary_metric"],
        display_metrics=tuple(payload.get("display_metrics", [])),
        allowed_edit_paths=tuple(payload.get("allowed_edit_paths", [payload["entry_file"]])),
        timeout_sec=payload.get("timeout_sec"),
        description=payload.get("description", ""),
        source=payload.get("source", ""),
    )


def load_task_catalog() -> list[TaskConfig]:
    return [load_task_config(_task_id(path.parent)) for path in _task_config_paths()]


def git_commit_short() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"
    return result.stdout.strip() or "unknown"


def relative_to_repo(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)
