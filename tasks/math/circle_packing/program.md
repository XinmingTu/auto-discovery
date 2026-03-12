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

## Files

Read:

- `tasks/math/circle_packing/task.json`
- `tasks/math/circle_packing/evaluator.py`
- `tasks/math/circle_packing/program.md`

Modify:

- `tasks/math/circle_packing/solve.py`

Do not edit any other file unless the human explicitly changes the rule.

## Ground truth

- `tasks/math/circle_packing/evaluator.py` is the ground truth.
- Judge changes only by verified evaluator output.
- Do not change the evaluator, runner, or task metadata to manufacture a better score.

## Run command

After each candidate change, run:

```bash
python scripts/run_task.py math/circle_packing --notes "<short experiment note>"
```

This appends a row to `tasks/math/circle_packing/results.tsv`.

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

Avoid unless clearly necessary:

- turning `solve.py` into a huge generic optimizer framework
- adding randomness without a clear reason
- changes that make the construction hard to understand while not improving the result

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

Suggested loop:

1. run the baseline once
2. edit `solve.py`
3. run the evaluator
4. if improved, commit the change
5. if not improved, revert `solve.py`
6. repeat

For regressions, prefer reverting only the task file, not the whole branch state.

## Experiment tactics

Promising directions:

- better boundary-aware layouts than simple concentric rings
- mixtures of center, boundary, and corner-focused circles
- slight asymmetry to exploit square edge effects
- small local coordinate surgery on a hand-designed layout
- improved radius assignment for a fixed center pattern
- parameterized templates with a few interpretable geometric constants

Less promising directions:

- broad refactors with no geometric hypothesis
- changing names or style only
- adding complexity that does not move `sum_radii`

## Operating mode

You are optimizing for verified result improvement, not for elegance.

A messy but effective geometric construction is better than a beautiful one that does not improve the score.

Do not stop after one idea if it fails. Iterate until you find a real improvement or exhaust the obvious geometric variants.
