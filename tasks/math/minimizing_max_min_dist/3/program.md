# Autonomous Task: minimizing_max_min_dist/3

You are an autonomous research agent working on one math optimization task.

Your goal is to improve the score for `tasks/math/minimizing_max_min_dist/3/solve.py`.

## Problem

Place exactly 14 points in 3 dimensions.

Objective:

- maximize `combined_score`
- the raw metric is `min_max_ratio = (d_min / d_max)^2`
- higher is better

Reference target:

- `min_max_ratio = 1 / 4.165849767`

## Setup

This task should run in a dedicated worktree branch, not on `main`.

Before doing experiments:

1. confirm the current branch with `git branch --show-current`
2. confirm the current directory with `pwd`
3. if you are on `main`, stop and tell the human to spawn a fresh worktree with:

```bash
python scripts/spawn_agents.py math/minimizing_max_min_dist/3
```

4. if you are already on a dedicated branch such as `autodiscovery/...`, continue
5. read the in-scope files listed below
6. run the baseline once before making any edits

## Files

Read:

- `tasks/math/minimizing_max_min_dist/3/task.json`
- `tasks/math/minimizing_max_min_dist/3/evaluator.py`
- `tasks/math/minimizing_max_min_dist/3/program.md`
- `tasks/math/minimizing_max_min_dist/3/seeds/seed_index.tsv`
- any seed snapshots under `tasks/math/minimizing_max_min_dist/3/seeds/` that look relevant

Modify:

- `tasks/math/minimizing_max_min_dist/3/solve.py`

Do not edit any other file unless the human explicitly changes the rule.

## Ground truth

- `tasks/math/minimizing_max_min_dist/3/evaluator.py` is the ground truth.
- Judge changes only by verified evaluator output.
- Do not change the evaluator, runner, or task metadata to manufacture a better score.

## Seed portfolio

This task may maintain several read-only seeds across runs.

Use them like this:

- read the seed archive for alternative point-set families
- combine ideas from multiple seeds mentally if useful
- implement the actual experiment only in `solve.py`

Do not edit the seed archive during a normal run.

## Run command

After each candidate change, run:

```bash
python scripts/run_task.py math/minimizing_max_min_dist/3 --notes "<short experiment note>"
```

This appends a row to `tasks/math/minimizing_max_min_dist/3/run_history.tsv`.

`tasks/math/minimizing_max_min_dist/3/results.tsv` is the curated milestone table on the main branch and should keep both `score` and raw `min_max_ratio` for readability.

Important printed fields:

- `score`
- `min_max_ratio`

## Baseline first

The first run in a fresh worktree should be the unmodified baseline:

```bash
python scripts/run_task.py math/minimizing_max_min_dist/3 --notes baseline
```

## Mutation policy

Default policy:

- only edit `solve.py`
- keep the solution self-contained
- do not add dependencies

Strong preference:

- explicit point constructions
- compact deterministic search heuristics inside `solve.py`
- real algorithmic help when it genuinely improves the configuration

## Allowed optimization methods

Examples:

- spherical or polyhedral initial layouts
- local perturbation search
- low-dimensional parameter search
- deterministic hill climbing
- lightweight numerical polishing
- symmetry-first constructions in 3D

## Forbidden shortcuts

Not allowed:

- editing `evaluator.py`
- editing `task.json`
- editing the runner or log files to fake a better score
- changing shapes or APIs to bypass validation

The only improvement that counts is a better verified result from the fixed evaluator.

## Keep / discard rule

Keep a change only if all of the following are true:

- the evaluator runs successfully
- the new `score` is strictly better than the current baseline in this worktree

If a change is worse, invalid, or crashes:

- discard it
- revert `solve.py`
- try another idea

## Git rule

This worktree is for one autonomous run.

Do not commit experimental changes on `main`.

Suggested loop:

1. run the baseline once
2. edit `solve.py`
3. run the evaluator
4. if improved, commit the change
5. if not improved, revert `solve.py`
6. repeat

## Experiment tactics

Promising directions:

- point sets on spheres with controlled radial perturbations
- polyhedral starting configurations
- maximizing symmetry first, then breaking it only where helpful
- local surgery on the pair controlling `d_min`
- hybrid construction plus numerical polishing

Less promising directions:

- style-only refactors
- broad abstractions with no geometric hypothesis
- extra complexity that does not move `min_max_ratio`
