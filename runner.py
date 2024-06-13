import asyncio
import sys
import inspect
import time
import types


# A decorator
def runner(func):
    def wrapper():
        print(f"\nSTART({func.__name__})")
        start = time.time()

        # Async Generator: These need to be run in
        # an async for loop.
        #
        # Since async for need awaiting they have to
        # be wrapped in another async function.
        #
        # Allows for niceties of generators and async
        # code.
        if inspect.isasyncgenfunction(func):

            async def async_runner():
                async for result in func():
                    log(func, result)
                return result

            result = asyncio.run(async_runner())

        # Async: These can be executed in a regular
        # function by using `asyncio.run`.
        #
        # This will run the function in a synchronous
        # context and return the value.
        #
        # This allows one to execute concurrent code
        # without handing over execution to a background
        # worker.
        elif inspect.iscoroutinefunction(func):

            async def func_func():
                sys.settrace(Logger(func).log)
                result = await func()
                sys.settrace(None)
                return result

            result = asyncio.run(func_func())

        # Generator: run in a regular for loop or by
        # using `next` these are pretty straight forward
        # yield is used as suspension points.
        elif inspect.isgeneratorfunction(func):
            for result in func():
                log(func, result)

        # Regular: These can be inspected using a tracer
        # tracer is more powerful but less simpler to use.
        else:
            sys.settrace(Logger(func).log)
            result = func()
            sys.settrace(None)

        print(f"STOP({func.__name__}) {time.time() - start:2.4}s")
        return result

    return wrapper


# Used to log intermediate values.
def log(func, value):
    print(f"\tINSP({func.__name__})", value)


# Used to log values if the function is not a
# generator, i.e. logging is done as a tracer.
class Logger:
    func: types.FunctionType
    counter: int

    def __init__(self, func) -> types.NoneType:
        self.func = func
        self.counter = 0

    def log(self, frame: types.FrameType, why, arg):
        frame.f_trace_opcodes = False
        frame.f_trace_lines = False

        if self.counter == 0:
            self.globals = set(frame.f_globals.keys())

        qualname = frame.f_code.co_qualname
        if why == "return" and (
            qualname != self.func.__name__
            and qualname in self.globals
            and not isinstance(arg, asyncio.Future)
        ):
            print(f"\tINSP({self.func.__name__})", arg)

        self.counter += 1
        return self.log
