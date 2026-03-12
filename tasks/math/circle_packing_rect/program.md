# Autonomous Task: circle_packing_rect

You are an autonomous research agent working on one math optimization task.

Your goal is to improve the score for `tasks/math/circle_packing_rect/solve.py`.

## Problem

Pack exactly 21 circles inside some rectangle whose perimeter is 4.

Constraints:

- no overlaps
- exactly 21 circles
- all radii must be nonnegative
- the full packing must fit inside a rectangle with `width + height <= 2`

Objective:

- maximize `combined_score`
- the raw metric is `radii_sum`
- higher is better

Reference target:

- `radii_sum = 2.3658321334167627`

## Setup

This task should run in a dedicated worktree branch, not on `main`.

Before doing experiments:

1. confirm the current branch with `git branch --show-current`
2. confirm the current directory with `pwd`
3. if you are on `main`, stop and tell the human to spawn a fresh worktree with:

```bash
python scripts/spawn_agents.py math/circle_packing_rect
```

4. if you are already on a dedicated branch such as `autodiscovery/...`, continue
5. read the in-scope files listed below
6. run the baseline once before making any edits

## Files

Read:

- `tasks/math/circle_packing_rect/task.json`
- `tasks/math/circle_packing_rect/evaluator.py`
- `tasks/math/circle_packing_rect/program.md`
- `tasks/math/circle_packing_rect/seeds/seed_index.tsv`
- any seed snapshots under `tasks/math/circle_packing_rect/seeds/` that look relevant

Modify:

- `tasks/math/circle_packing_rect/solve.py`

Do not edit any other file unless the human explicitly changes the rule.

## Ground truth

- `tasks/math/circle_packing_rect/evaluator.py` is the ground truth.
- Judge changes only by verified evaluator output.
- Do not change the evaluator, runner, or task metadata to manufacture a better score.

## Seed portfolio

This task may maintain several read-only seeds across runs.

Use them like this:

- read the seed archive for alternative packing families
- combine ideas from multiple seeds mentally if useful
- implement the actual experiment only in `solve.py`

Do not edit the seed archive during a normal run.

## Run command

After each candidate change, run:

```bash
python scripts/run_task.py math/circle_packing_rect --notes "<short experiment note>"
```

This appends a row to `tasks/math/circle_packing_rect/run_history.tsv`.

`tasks/math/circle_packing_rect/results.tsv` is the curated milestone table on the main branch and should keep both `score` and raw `radii_sum` for readability.

Important printed fields:

- `score`
- `radii_sum`

## Baseline first

The first run in a fresh worktree should be the unmodified baseline:

```bash
python scripts/run_task.py math/circle_packing_rect --notes baseline
```

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

## Mutation policy

Default policy:

- only edit `solve.py`
- keep the solution self-contained
- do not add dependencies

Strong preference:

- explicit geometric constructions
- compact local heuristics inside `solve.py`
- real algorithmic help when it genuinely improves the packing

## Allowed optimization methods

You are allowed to use actual optimization ideas inside `solve.py` if they help.

Examples:

- fixed-layout templates with tunable coordinates and radii
- low-dimensional parameter search for row or shell patterns
- local center perturbation
- deterministic hill climbing
- lightweight numerical polishing
- rectangle aspect-ratio tuning coupled to the packing layout

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

## Experiment tactics

Promising directions:

- asymmetric row layouts
- boundary-aware placements that exploit the flexible rectangle shape
- mixtures of larger central circles and smaller edge circles
- compact parameterized templates with a few interpretable geometry constants
- hybrid construction plus numerical polishing

Less promising directions:

- style-only refactors
- broad abstractions with no geometric hypothesis
- extra complexity that does not move `radii_sum`
