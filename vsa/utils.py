import functools
import statistics
import time
from contextlib import contextmanager
from typing import List, Any, Callable, Generator, Optional

def collect_stats(func: Callable[..., Any], runs: int = 10) -> dict:
    times: List[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)
    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
    }

@contextmanager
def timer() -> Generator[None, None, float]:
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        print(f"Execution time: {end_time - start_time:.6f} seconds")

#https://claude.ai/chat/c925cd4d-c149-4526-ade7-8a947a589c4a
def timer_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            print(f"{func.__name__} execution time: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

class CountCalls:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__}")
        return self.func(*args, **kwargs)

class CallableResult:

    def __init__(self,
                 output: Any = None,
                 error: Optional[Exception] = None,
                 time: Optional[float] = None):
        self.output = output
        self.error = error
        self.time = time

    def __repr__(self):
        if self.error:
            return f"{self.error}\n{self.time}"
        return f"{self.output}\n{self.time}"


def mr_timer(fun: Callable, *args, **kwargs) -> Any:
    start_time = time.time()
    try:
        output = fun(*args, **kwargs)
    except Exception as e:
        output = str(e)
        end_time = time.time() - start_time
        return CallableResult(error=e, time=end_time)
    end_time = time.time() - start_time
    return CallableResult(output=output, time=end_time)
