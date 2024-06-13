import asyncio
import random
import time
from runner import runner


@runner
async def async_job():
    val_one = await async_task("one", 0.0)

    # Concurrently running independent tasks
    vals_two = await asyncio.gather(
        async_task("two-a", val_one),
        async_task("two-b", val_one),
    )
    return await async_task("three", sum(vals_two))


@runner
async def async_gen_job():
    yield (val_one := await async_task("one", 0.0))

    # Concurrently running independent tasks
    yield (
        vals_two := await asyncio.gather(
            async_task("two-a", val_one),
            async_task("two-b", val_one),
        )
    )
    yield await async_task("three", sum(vals_two))


@runner
def sync_job():
    val_one = sync_task("one", 0.0)
    vals_two = [
        sync_task("two-a", val_one),
        sync_task("two-b", val_one),
    ]
    return sync_task("three", sum(vals_two))


@runner
def sync_gen_job():
    yield (val_one := sync_task("one", 0.0))
    yield (
        vals_two := [
            sync_task("two-a", val_one),
            sync_task("two-b", val_one),
        ]
    )
    yield sync_task("three", sum(vals_two))


async def async_task(name, val: float):
    await asyncio.sleep(1)
    print("step done:", name)
    return random.random() + val


def sync_task(name, val: float):
    time.sleep(1)
    print("step done:", name)
    return random.random() + val
