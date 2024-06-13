### Incomplete ideas for a Python job runner

Given a function which encapsulates a **job**, wherein the contents of the **job** can be regarded as the job's **steps**, a job runner should be able to:

1. Pause execution after a step.
   - `yield` can be used as a suspension point.
   - Registered trace function (`sys.settrace`) can pause function, but it runs as a callback.
2. Log output/outcome of a step, even if it throws an error.
   - `[partial]` `yield` can be handover the value of a step.
   - `[partial]` Registered trace function (`sys.settrace`) can log
3. Resume execution after Pause.
   - Generator functions (`yield`) can be resumed by calling `next`.
   - Execution resumes when trace function returns.
4. Resume execution from any arbitrary step in the function using some saved state.
   - Not yet found a method.

**Nice to haves**: be able to execute concurrent steps.

- Using `asyncio.gather` to run concurrent async functions
- Above can be used with `yield` to have a suspend-able async generator function.
