import asyncio
import inspect
import time
import jobs


def job_runner(func):
    def wrapper():
        print(f"\nSTART({func.__name__})")
        start = time.time()

        if inspect.isasyncgenfunction(func):

            async def async_runner():
                async for result in func():
                    print(f"\tINSP({func.__name__})", result)
                return result

            result = asyncio.run(async_runner())
        elif inspect.iscoroutinefunction(func):
            result = asyncio.run(func())
            print(f"\tINSP({func.__name__})", result)
        elif inspect.isgeneratorfunction(func):
            for result in func():
                print(f"\tINSP({func.__name__})", result)
        else:
            result = func()
            print(f"\tINSP({func.__name__})", result)

        print(f"STOP({func.__name__}) {time.time() - start:2.4}s")
        return result

    return wrapper


async_job = job_runner(jobs.async_job)
print(async_job())

sync_job = job_runner(jobs.sync_job)
print(sync_job())

sync_gen_job = job_runner(jobs.sync_gen_job)
print(sync_gen_job())

async_gen_job = job_runner(jobs.async_gen_job)
print(async_gen_job())
