# Task contract

Each task lives in its own directory under `tasks/`.

## Required files

- `task.json`
- `program.md`
- `evaluator.py`
- the mutable solution file referenced by `entry_file`

## `task.json`

Required keys:

```json
{
  "name": "circle_packing",
  "domain": "math",
  "objective": "maximize",
  "entry_file": "solve.py",
  "evaluator_file": "evaluator.py",
  "primary_metric": "combined_score",
  "allowed_edit_paths": ["solve.py"]
}
```

Optional keys:

- `display_metrics`: numeric metrics to print after each run
- `timeout_sec`: evaluator-side timeout budget
- `description`: short human description
- `source`: where the task was imported from

## Evaluator contract

`evaluator.py` must define:

```python
def evaluate(program_path: str) -> dict:
    ...
```

The returned dict should contain the configured `primary_metric`. This mirrors the SkyDiscover evaluator shape, so imported math tasks can stay close to upstream.

## Mutation rule

The default rule is strict: Codex should only edit the files listed in `allowed_edit_paths`. For imported math tasks, that should usually be exactly one file.
