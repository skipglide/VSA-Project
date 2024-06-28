import functools
import statistics
import time
from contextlib import contextmanager
from typing import List, Any, Callable, Generator, Optional

# https://book.pythontips.com/en/latest/context_managers.html

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


class TimeCalls:
    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.runs = []

    def __call__(self, *args, **kwargs):
        start_time = time.perf_counter()
        result = self.func(*args, **kwargs)
        self.runs.append(start - time.perf_counter())
        return result
    
    def stats(self):
        return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
        }
