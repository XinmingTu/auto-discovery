# auto-discovery

`auto-discovery` is a tiny multi-task research runner for Codex focused on self-contained math optimization tasks. It keeps the `autoresearch` workflow that matters most:

- one task at a time
- one mutable solution file per task
- fixed evaluator
- local result logging
- easy fan-out via `git worktree`

The benchmark source of truth can stay in `references/`, but the runnable tasks in this repo are self-contained. `references/` is ignored by git on purpose.

This repo is intentionally small. It is not trying to reimplement the full SkyDiscover search stack or a full agent framework. The goal is a hackable middle ground: import useful benchmarks, keep evaluators fixed, and let Codex iterate directly against `program.md` plus one mutable task file.

Evaluators and several task scaffolds in `tasks/math/` are adapted from the SkyDiscover benchmark definitions, then repackaged into self-contained task directories for this repo.

## Related repos

`auto-discovery` borrows ideas from three related projects:

| Project | What it emphasizes | How `auto-discovery` is positioned |
| --- | --- | --- |
| [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch) | A very small autonomous research loop around one mutable training file, a fixed evaluator, and a short time budget. | We borrow the core discipline: one mutable file, fixed evaluation, and `program.md` as the main control surface. |
| [`skydiscover-ai/skydiscover`](https://github.com/skydiscover-ai/skydiscover) | A modular framework for AI-driven scientific and algorithmic discovery across 200+ optimization tasks and multiple search algorithms. | We borrow the benchmark style and evaluator contract, but keep the runner much thinner and more Codex-native. |
| [`baidu-baige/LoongFlow`](https://github.com/baidu-baige/LoongFlow) | A broader thinking-and-learning agent framework built around the PES paradigm for expert-grade agents. | We take a lighter approach: task-local `program.md`, fixed evaluators, and git worktrees instead of a larger general-purpose agent framework. |

## Current focus

The current scope is intentionally narrow:

- imported math optimization tasks, mostly from SkyDiscover
- fixed evaluator plus one mutable `solve.py` per task
- task-local `program.md` as the main Codex instruction surface
- git worktrees for parallel runs when needed

That makes the repo easy to fork, easy to inspect, and easy to run with a bare Codex session.

## Comparison on overlapping tasks

Below is the current comparison on tasks where `auto-discovery` already has promoted non-baseline results on `main`.

- For `circle_packing`, `circle_packing_rect`, and `heilbronn_triangle`, higher is better.
- For `minimizing_max_min_dist/2` and `minimizing_max_min_dist/3`, the table uses the inverse metric `(d_max / d_min)^2`, so lower is better. This matches how LoongFlow reports these distance tasks.
- `SkyDiscover` values below are the best published values across the AdaEvolve blog/paper and the EvoX paper for the overlapping tasks.
- `-` means the cited published source set does not report that exact task/result pair.
- This is a useful reference table, not a perfectly controlled apples-to-apples benchmark: the published systems use different backbones and reporting conventions, and some paper tables round values aggressively.

| Method | Circle Packing Square `n=26` `↑` | Circle Packing Rectangle `n=21` `↑` | Heilbronn Triangle `n=11` `↑` | Inverse Max/Min Dist `n=16,d=2` `↓` | Inverse Max/Min Dist `n=14,d=3` `↓` |
| --- | --- | --- | --- | --- | --- |
| AlphaEvolve | `2.6358627564136983` | `2.3658321334167627` | `0.036529889880030156` | `12.88926611203463` | `4.165849767` |
| SkyDiscover (best published AdaEvolve/EvoX) | `2.63598308` | `2.36583237` | `0.036` | `-` | `4.16579879192` |
| LoongFlow | `2.6359829624734026` | `2.365832229500823` | `0.0365298898793351` | `12.889243547212832` | `-` |
| auto-discovery | `2.63598308911` | `2.36584169299` | `0.03652988988` | `12.8892299077` | `4.16578347458007` |

Current task-local milestone files:

- [`tasks/math/circle_packing/results.tsv`](tasks/math/circle_packing/results.tsv)
- [`tasks/math/circle_packing_rect/results.tsv`](tasks/math/circle_packing_rect/results.tsv)
- [`tasks/math/heilbronn_triangle/results.tsv`](tasks/math/heilbronn_triangle/results.tsv)
- [`tasks/math/minimizing_max_min_dist/2/results.tsv`](tasks/math/minimizing_max_min_dist/2/results.tsv)
- [`tasks/math/minimizing_max_min_dist/3/results.tsv`](tasks/math/minimizing_max_min_dist/3/results.tsv)

Published comparison sources:

- [SkyDiscover blog](https://skydiscover-ai.github.io/blog.html)
- [AdaEvolve paper](https://arxiv.org/pdf/2602.20133)
- [EvoX paper](https://arxiv.org/pdf/2602.23413)
- [LoongFlow README](https://github.com/baidu-baige/LoongFlow)

## Validating the results

The promoted `auto-discovery` values in the table above are meant to be reproducible from the checked-in task files on `main`.

To validate a result locally, run the fixed evaluator for the corresponding task:

```bash
python scripts/run_task.py math/circle_packing
python scripts/run_task.py math/circle_packing_rect
python scripts/run_task.py math/heilbronn_triangle
python scripts/run_task.py math/minimizing_max_min_dist/2
python scripts/run_task.py math/minimizing_max_min_dist/3
```

What to compare:

- `circle_packing`: compare `sum_radii`
- `circle_packing_rect`: compare `radii_sum`
- `heilbronn_triangle`: compare `min_area_normalized`
- `minimizing_max_min_dist/2`: compare `inverse_min_max_ratio`
- `minimizing_max_min_dist/3`: compare `inverse_min_max_ratio`

The exact milestone history for each promoted result is tracked in that task's `results.tsv`. If a value in `main` changes, rerun the corresponding command and update both the task-local `results.tsv` and the comparison table in this README.

## Layout

```text
tasks/
  math/
    circle_packing/
      task.json
      program.md
      evaluator.py
      solve.py
      seeds/
        seed_index.tsv
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

`python scripts/run_task.py ...` appends raw local evaluations to `run_history.tsv`. Each task's tracked `results.tsv` is reserved for curated milestones that you want visible on GitHub, and can use task-specific human-friendly columns such as both normalized score and raw objective value.

## Task contract

Each task directory contains:

- `task.json`: machine-readable task metadata
- `program.md`: Codex instructions for the task
- `evaluator.py`: fixed evaluator exposing `evaluate(program_path)`
- `solve.py`: the file Codex is expected to improve

Tasks may also keep a small read-only seed archive under `seeds/`. This supports multiple construction families across runs without letting one run edit the whole archive.

The framework uses JSON instead of YAML for task metadata so the runner stays dependency-free on Python 3.10+.

See [docs/task-contract.md](/homes/gws/tuxm/Project/auto-discovery/docs/task-contract.md) and [docs/skydiscover-math-inventory.md](/homes/gws/tuxm/Project/auto-discovery/docs/skydiscover-math-inventory.md).
