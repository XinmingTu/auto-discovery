# Autonomous Task: minimizing_max_min_dist/2

You are an autonomous research agent working on one math optimization task.

Your goal is to improve the score for `tasks/math/minimizing_max_min_dist/2/solve.py`.

## Problem

Place exactly 16 points in 2 dimensions.

Objective:

- maximize `combined_score`
- the raw metric is `min_max_ratio = (d_min / d_max)^2`
- higher is better

Reference target:

- `min_max_ratio = 1 / 12.889266112`

## Setup

This task should run in a dedicated worktree branch, not on `main`.

Before doing experiments:

1. confirm the current branch with `git branch --show-current`
2. confirm the current directory with `pwd`
3. if you are on `main`, stop and tell the human to spawn a fresh worktree with:

```bash
python scripts/spawn_agents.py math/minimizing_max_min_dist/2
```

4. if you are already on a dedicated branch such as `autodiscovery/...`, continue
5. read the in-scope files listed below
6. run the baseline once before making any edits

## Files

Read:

- `tasks/math/minimizing_max_min_dist/2/task.json`
- `tasks/math/minimizing_max_min_dist/2/evaluator.py`
- `tasks/math/minimizing_max_min_dist/2/program.md`
- `tasks/math/minimizing_max_min_dist/2/seeds/seed_index.tsv`
- any seed snapshots under `tasks/math/minimizing_max_min_dist/2/seeds/` that look relevant

Modify:

- `tasks/math/minimizing_max_min_dist/2/solve.py`

Do not edit any other file unless the human explicitly changes the rule.

## Ground truth

- `tasks/math/minimizing_max_min_dist/2/evaluator.py` is the ground truth.
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
python scripts/run_task.py math/minimizing_max_min_dist/2 --notes "<short experiment note>"
```

This appends a row to `tasks/math/minimizing_max_min_dist/2/run_history.tsv`.

`tasks/math/minimizing_max_min_dist/2/results.tsv` is the curated milestone table on the main branch and should keep both `score` and raw `min_max_ratio` for readability.

Important printed fields:

- `score`
- `min_max_ratio`

## Baseline first

The first run in a fresh worktree should be the unmodified baseline:

```bash
python scripts/run_task.py math/minimizing_max_min_dist/2 --notes baseline
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

- normalized point configurations
- local perturbation search
- spherical or lattice-inspired initial layouts
- low-dimensional parameter search
- deterministic hill climbing
- lightweight numerical polishing

## Forbidden shortcuts

Not allowed:

- editing `evaluator.py`
- editing `task.json`
- editing the runner or log files to fake a better score
- searching the web for direct answers, published coordinates, benchmark-specific solutions, or existing final constructions
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

- near-uniform point sets on normalized shapes
- projecting points to spheres or circles before affine distortion
- maximizing symmetry first, then breaking it only where helpful
- local surgery on the pair controlling `d_min`
- hybrid construction plus numerical polishing

Less promising directions:

- style-only refactors
- broad abstractions with no geometric hypothesis
- extra complexity that does not move `min_max_ratio`
