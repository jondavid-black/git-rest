import time
from collections.abc import Callable
from typing import Any


class PerformanceMetrics:
    @staticmethod
    def time_operation(func: Callable, *args, **kwargs) -> tuple[Any, float]:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = end - start
        return result, duration

    @staticmethod
    def is_within_threshold(duration: float, threshold: float = 2.0) -> bool:
        return duration <= threshold
