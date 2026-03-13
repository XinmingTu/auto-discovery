# auto-discovery

**An exploratory, minimalist scaffold for LLM-driven discovery algorithms.**

Inspired by [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch) and [`skydiscover-ai/skydiscover`](https://github.com/skydiscover-ai/skydiscover), this repository starts from a simple question:

if we want an LLM like Codex to act as a discovery agent on math optimization tasks, do we really need a massive, heavy-duty framework, or can a much smaller scaffold already get us most of the useful behavior?

`auto-discovery` is an attempt to answer that in the smallest practical way. It is not a fully fledged production framework. It is a hackable sandbox built around a simple bet: a file-based setup with strong task-local instructions, a fixed evaluator, and a small amount of git discipline may already be enough to make LLMs iterate usefully and discover competitive solutions.

The repo itself is part of that experiment. `auto-discovery` is also being built in a Codex-first, vibe-research / vibe-coding style: the agent is not only used on the benchmark tasks, but also used to shape the scaffold, the task conventions, the documentation, and the iteration workflow around them.

Most of the current experiments and repo iteration here have been run with Codex using GPT-5.4 xhigh.

Evaluators and several task scaffolds in `tasks/math/` are adapted from the SkyDiscover benchmark definitions, then repackaged into self-contained task directories for this repo. The benchmark source of truth can stay in `references/`, but the runnable tasks here are entirely self-contained. `references/` is ignored by git on purpose.

## Exploratory results

Despite its minimal nature, this scaffold has already produced competitive results on several imported math optimization tasks.

Note on rigor:

- The tables below are directional references, not a strictly controlled apples-to-apples benchmark.
- External systems use different LLM backbones, search budgets, and reporting conventions.
- Some published numbers are rounded aggressively, so tiny gaps or ties may be hidden by display precision.
- Bold marks the numerically best shown method/value in each task table.

Metric conventions:

- For `circle_packing`, `circle_packing_rect`, and `heilbronn_triangle`, higher is better.
- For `minimizing_max_min_dist/2` and `minimizing_max_min_dist/3`, the table uses the inverse metric `(d_max / d_min)^2`, so lower is better.
- `-` means the published source I checked does not report that exact task/result pair.

### Circle Packing Square `n=26` `↑`

| Method | Value | Source |
| :--- | :--- | :--- |
| AlphaEvolve | `2.6358627564136983` | [LoongFlow README](https://github.com/baidu-baige/LoongFlow) |
| SkyDiscover (best published AdaEvolve/EvoX) | `2.63598308` | [AdaEvolve paper](https://arxiv.org/pdf/2602.20133) |
| LoongFlow | `2.6359829624734026` | [LoongFlow README](https://github.com/baidu-baige/LoongFlow) |
| **auto-discovery** | **`2.63598308911`** | [results.tsv](tasks/math/circle_packing/results.tsv) |

### Circle Packing Rectangle `n=21` `↑`

| Method | Value | Source |
| :--- | :--- | :--- |
| AlphaEvolve | `2.3658321334167627` | [LoongFlow README](https://github.com/baidu-baige/LoongFlow) |
| SkyDiscover (best published AdaEvolve/EvoX) | `2.36583237` | [SkyDiscover blog](https://skydiscover-ai.github.io/blog.html) |
| LoongFlow | `2.365832229500823` | [LoongFlow README](https://github.com/baidu-baige/LoongFlow) |
| **auto-discovery** | **`2.36584169299`** | [results.tsv](tasks/math/circle_packing_rect/results.tsv) |

### Heilbronn Triangle `n=11` `↑`

| Method | Value | Source |
| :--- | :--- | :--- |
| **AlphaEvolve** | **`0.036529889880030156`** | [LoongFlow README](https://github.com/baidu-baige/LoongFlow) |
| SkyDiscover (best published AdaEvolve/EvoX) | `0.036` | [AdaEvolve paper](https://arxiv.org/pdf/2602.20133) |
| LoongFlow | `0.0365298898793351` | [LoongFlow README](https://github.com/baidu-baige/LoongFlow) |
| **auto-discovery** | **`0.036529889880030156`** | [results.tsv](tasks/math/heilbronn_triangle/results.tsv) |

### Inverse Max/Min Dist `n=16,d=2` `↓`

| Method | Value | Source |
| :--- | :--- | :--- |
| AlphaEvolve | `12.88926611203463` | [LoongFlow README](https://github.com/baidu-baige/LoongFlow) |
| SkyDiscover (best published AdaEvolve/EvoX) | `12.89` | [EvoX paper](https://arxiv.org/pdf/2602.23413) |
| LoongFlow | `12.889243547212832` | [LoongFlow README](https://github.com/baidu-baige/LoongFlow) |
| **auto-discovery** | **`12.8892299077`** | [results.tsv](tasks/math/minimizing_max_min_dist/2/results.tsv) |

### Inverse Max/Min Dist `n=14,d=3` `↓`

| Method | Value | Source |
| :--- | :--- | :--- |
| AlphaEvolve | `4.165849767` | [SkyDiscover blog](https://skydiscover-ai.github.io/blog.html) |
| SkyDiscover (best published AdaEvolve/EvoX) | `4.16579879192` | [SkyDiscover blog](https://skydiscover-ai.github.io/blog.html) |
| LoongFlow | `-` | `-` |
| **auto-discovery** | **`4.16578347458007`** | [results.tsv](tasks/math/minimizing_max_min_dist/3/results.tsv) |

## The minimal setup

Instead of reimplementing a full search stack, `auto-discovery` strips the process down to its essentials. The workflow is decentralized into self-contained task directories:

- `program.md`: a strong, task-local instruction surface and context for the LLM
- `solve.py`: the single mutable solution file the LLM is expected to improve
- `evaluator.py`: a fixed, objective evaluation script
- `git worktree`: native support for isolated parallel runs and milestone tracking

This makes the repo easy to fork, inspect, and run directly with a bare LLM session.

## Quick start

The framework is designed to be runnable out of the box.

```bash
# List all available tasks
python scripts/list_tasks.py

# Run a baseline evaluation for a specific task
python scripts/run_task.py math/circle_packing --notes baseline

# Spawn agents in isolated git worktrees
python scripts/spawn_agents.py math/circle_packing
```

- `spawn_agents.py` creates one git worktree per task and prints the LLM prompt to use in that worktree.
- `run_task.py` appends raw local evaluations to `run_history.tsv`.
- Each task's tracked `results.tsv` is reserved for curated milestones you want visible on GitHub.

## Validating the results

The promoted `auto-discovery` values recorded in each task's `results.tsv` are reproducible from the checked-in task files on `main`.

To validate a result locally, run the fixed evaluator for the corresponding task:

```bash
python scripts/run_task.py math/circle_packing
python scripts/run_task.py math/circle_packing_rect
python scripts/run_task.py math/heilbronn_triangle
python scripts/run_task.py math/minimizing_max_min_dist/2
python scripts/run_task.py math/minimizing_max_min_dist/3
```

What to compare:

- `circle_packing`: `sum_radii`
- `circle_packing_rect`: `radii_sum`
- `heilbronn_triangle`: `min_area_normalized`
- `minimizing_max_min_dist/2`: `inverse_min_max_ratio`
- `minimizing_max_min_dist/3`: `inverse_min_max_ratio`

The exact milestone history for each promoted result is tracked in that task's `results.tsv`. If a value on `main` changes, rerun the corresponding command and update the task-local milestone record.

## Layout and task contract

The runnable tasks in this repo are self-contained, even if the benchmark source of truth lives in `references/`.

```text
tasks/
  math/
    circle_packing/
      task.json         # Machine-readable task metadata
      program.md        # LLM instructions for the task
      evaluator.py      # Fixed evaluator exposing `evaluate(program_path)`
      solve.py          # The file the LLM is expected to improve
      seeds/
        seed_index.tsv  # Small read-only seed archive
scripts/
  _tasks.py
  list_tasks.py
  run_task.py
  spawn_agents.py
references/
docs/
```

The framework uses JSON instead of YAML for task metadata to keep the runner dependency-free on Python 3.10+.

For deeper details, see [docs/task-contract.md](/homes/gws/tuxm/Project/auto-discovery/docs/task-contract.md) and [docs/skydiscover-math-inventory.md](/homes/gws/tuxm/Project/auto-discovery/docs/skydiscover-math-inventory.md).

## Related repositories

`auto-discovery` builds on and borrows ideas from:

- [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch)
- [`skydiscover-ai/skydiscover`](https://github.com/skydiscover-ai/skydiscover)
- [`baidu-baige/LoongFlow`](https://github.com/baidu-baige/LoongFlow)
