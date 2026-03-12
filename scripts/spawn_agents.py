from __future__ import annotations

import argparse
import subprocess
from datetime import datetime
from pathlib import Path

from _tasks import REPO_ROOT, load_task_config, relative_to_repo


def _git_stdout(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_run(*args: str) -> None:
    subprocess.run(["git", *args], cwd=REPO_ROOT, check=True)


def _default_prompt(task_id: str, entry_file: str) -> str:
    return (
        f"Read tasks/{task_id}/program.md and iteratively improve tasks/{task_id}/{entry_file}. "
        f"Use `python scripts/run_task.py {task_id}` after each change. "
        f"Only edit the allowed task file(s) unless the task instructions say otherwise. "
        f"Commit verified improvements and discard regressions."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create one git worktree per task for Codex runs.")
    parser.add_argument("tasks", nargs="+", help="Task ids like math/circle_packing")
    parser.add_argument(
        "--root",
        default="runs/worktrees",
        help="Worktree root relative to the repository root.",
    )
    parser.add_argument(
        "--branch-prefix",
        default="autodiscovery",
        help="Prefix used for new worktree branches.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow spawning from a dirty checkout. Worktrees still start from HEAD only.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands without creating worktrees.")
    args = parser.parse_args()

    if not args.allow_dirty and _git_stdout("status", "--short"):
        raise SystemExit(
            "Refusing to spawn worktrees from a dirty checkout. Commit or stash first, or rerun with --allow-dirty."
        )

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    worktree_root = (REPO_ROOT / args.root).resolve()

    for index, task_ref in enumerate(args.tasks, start=1):
        task = load_task_config(task_ref)
        slug = task.task_id.replace("/", "-")
        branch = f"{args.branch_prefix}/{stamp}-{slug}-{index:02d}"
        worktree_path = worktree_root / slug / f"{stamp}-{index:02d}"
        worktree_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"task: {task.task_id}")
        print(f"branch: {branch}")
        print(f"worktree: {relative_to_repo(worktree_path)}")
        print(f"prompt: {_default_prompt(task.task_id, task.entry_file)}")

        if args.dry_run:
            print(
                f"command: git worktree add -b {branch} {worktree_path} HEAD"
            )
            print()
            continue

        _git_run("worktree", "add", "-b", branch, str(worktree_path), "HEAD")
        print()


if __name__ == "__main__":
    main()
