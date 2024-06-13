# Simple Python Job Runner

Given a function which encapsulates a **job**, where in the contents of the **job** can be regarded as the job's **steps**, be able to:

1. Pause the execution after a step.
   - `yield` can be used as a suspension point.
2. Inspect the output/outcome of a step, even if it throws an error.
   - `yield` can be handover the value of a step.
3. Resume execution after Pause.
   - Generator functions (`yield`) can be resumed by calling `next`
4. Resume execution from any arbitrary step in the function using some saved state.
   - Not yet found a method.

**Niceties**: be able to execute concurrent steps.

- Using `asyncio.gather` to run concurrent async functions
- Above can be used with `yield` to have a suspend-able async generator function.
