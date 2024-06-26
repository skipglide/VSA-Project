import time
from typing import Any, Callable, Optional

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
