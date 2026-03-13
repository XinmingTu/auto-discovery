# Autonomous Task: circle_packing

You are an autonomous research agent working on one math optimization task.

Your goal is to improve the score for `tasks/math/circle_packing/solve.py`.

## Problem

Pack exactly 26 circles inside the unit square.

Constraints:

- no overlaps
- every circle must lie fully inside the square
- exactly 26 circles

Objective:

- maximize `combined_score`
- the most interpretable raw metric is `sum_radii`
- higher is better

Reference target:

- `sum_radii = 2.635`

## Setup

This task should run in a dedicated worktree branch, not on `main`.

Before doing experiments:

1. confirm the current branch with `git branch --show-current`
2. confirm the current directory with `pwd`
3. if you are on `main`, stop and tell the human to spawn a fresh worktree with:

```bash
python scripts/spawn_agents.py math/circle_packing
```

4. if you are already on a dedicated branch such as `autodiscovery/...`, continue
5. read the in-scope files listed below
6. run the baseline once before making any edits

## Files

Read:

- `tasks/math/circle_packing/task.json`
- `tasks/math/circle_packing/evaluator.py`
- `tasks/math/circle_packing/program.md`
- `tasks/math/circle_packing/seeds/seed_index.tsv`
- any seed snapshots under `tasks/math/circle_packing/seeds/` that look relevant

Modify:

- `tasks/math/circle_packing/solve.py`

Do not edit any other file unless the human explicitly changes the rule.

## Ground truth

- `tasks/math/circle_packing/evaluator.py` is the ground truth.
- Judge changes only by verified evaluator output.
- Do not change the evaluator, runner, or task metadata to manufacture a better score.

## Seed portfolio

This task may maintain several read-only seeds across runs.

Use them like this:

- read the seed archive for alternative construction families
- combine ideas from multiple seeds mentally if useful
- implement the actual experiment only in `solve.py`

Do not edit the seed archive during a normal run.

The seed archive is for cross-run diversity. The current run still has one mutable file.

## Run command

After each candidate change, run:

```bash
python scripts/run_task.py math/circle_packing --notes "<short experiment note>"
```

This appends a row to `tasks/math/circle_packing/run_history.tsv`.

`tasks/math/circle_packing/results.tsv` is the curated milestone table on the main branch and should keep both `score` and raw `sum_radii` for readability.

Important printed fields:

- `score`
- `sum_radii`
- `validity`

## Baseline first

The first run in a fresh worktree should be the unmodified baseline:

```bash
python scripts/run_task.py math/circle_packing --notes baseline
```

Record that number mentally before making changes.

## Mutation policy

Default policy:

- only edit `solve.py`
- keep the solution self-contained
- do not add dependencies

Strong preference:

- explicit geometric constructions
- compact local heuristics inside `solve.py`
- real algorithmic help when it genuinely improves the packing

Avoid unless clearly necessary:

- turning `solve.py` into a huge generic optimizer framework
- adding randomness without a clear reason
- changes that make the construction hard to understand while not improving the result

## Allowed optimization methods

You are allowed to use actual optimization ideas inside `solve.py` if they help.

Examples:

- small local search over circle centers
- coordinate descent
- deterministic hill climbing
- low-dimensional parameter search
- sequential linear programming style updates
- lightweight numerical refinement after constructing a layout
- helper functions that analyze overlaps, slack, or boundary pressure

This is encouraged when it improves the verified evaluator result.

## Forbidden shortcuts

Do not try to improve the score by changing what is being measured.

Not allowed:

- editing `evaluator.py`
- editing `task.json`
- editing the runner or log files to fake a better score
- searching the web for direct answers, published coordinates, benchmark-specific solutions, or existing final constructions
- returning a fake `reported_sum`
- changing output shapes or APIs to bypass validation

The only improvement that counts is a better verified result from the fixed evaluator.

## Keep / discard rule

Keep a change only if all of the following are true:

- the evaluator runs successfully
- `validity` stays `1`
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

For regressions, prefer reverting only the task file, not the whole branch state.

If you discover a genuinely different strong construction family, note that in the commit message or run notes so it can be promoted to a new seed later.

## Experiment tactics

Promising directions:

- better boundary-aware layouts than simple concentric rings
- mixtures of center, boundary, and corner-focused circles
- slight asymmetry to exploit square edge effects
- small local coordinate surgery on a hand-designed layout
- improved radius assignment for a fixed center pattern
- parameterized templates with a few interpretable geometric constants
- hybrid construction plus numerical polishing
- simple search procedures that adjust a compact set of geometry parameters

Less promising directions:

- broad refactors with no geometric hypothesis
- changing names or style only
- adding complexity that does not move `sum_radii`

## Operating mode

You are optimizing for verified result improvement, not for elegance.

A messy but effective geometric construction is better than a beautiful one that does not improve the score.

Do not stop after one idea if it fails. Iterate until you find a real improvement or exhaust the obvious geometric variants.
