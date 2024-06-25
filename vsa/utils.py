import time
from typing import Any, Callable, Optional


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
