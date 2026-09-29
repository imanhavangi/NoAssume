# "Fix the bug where orders on the last day are excluded"

`orders.py` uses `date < end` instead of `date <= end`. Nearby, an unrelated
`refund_total()` sums floats.

## Without NoAssume

The diff fixes the off-by-one — and "while in there" rewrites
`refund_total()` to use Decimal, changes its rounding, and touches three
call sites. The PR now carries an unreviewed behavior change inside a bugfix.

## With NoAssume

The bug is specific — clarification is cheap. The fix lands, a regression
test matching the suite's conventions lands beside it.

While implementing, the agent notices `refund_total()`. The guard treats it
as out-of-scope temptation:

```text
Noticed while implementing: refund_total() sums floats (possible precision
bug, unrelated to this fix). Left untouched — file it or say the word and
I'll fix it separately.
```

The suggestion surfaces without the drift. The audit confirms: one
decision, one fix, zero collateral.
