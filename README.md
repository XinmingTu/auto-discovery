# auto-discovery

`auto-discovery` is a tiny multi-task research runner for Codex. It keeps the `autoresearch` workflow that matters most:

- one task at a time
- one mutable solution file per task
- fixed evaluator
- local result logging
- easy fan-out via `git worktree`

The benchmark source of truth can stay in `references/`, but the runnable tasks in this repo are self-contained. `references/` is ignored by git on purpose.

## Layout

```text
tasks/
  math/
    circle_packing/
      task.json
      program.md
      evaluator.py
      solve.py
scripts/
  _tasks.py
  list_tasks.py
  run_task.py
  spawn_agents.py
references/
docs/
```

## Quick start

```bash
python scripts/list_tasks.py
python scripts/run_task.py math/circle_packing --notes baseline
python scripts/spawn_agents.py math/circle_packing
```

`spawn_agents.py` creates one git worktree per task and prints the Codex prompt to use in that worktree.

## Task contract

Each task directory contains:

- `task.json`: machine-readable task metadata
- `program.md`: Codex instructions for the task
- `evaluator.py`: fixed evaluator exposing `evaluate(program_path)`
- `solve.py`: the file Codex is expected to improve

The framework uses JSON instead of YAML for task metadata so the runner stays dependency-free on Python 3.10+.

See [docs/task-contract.md](/homes/gws/tuxm/Project/auto-discovery/docs/task-contract.md) and [docs/skydiscover-math-inventory.md](/homes/gws/tuxm/Project/auto-discovery/docs/skydiscover-math-inventory.md).
