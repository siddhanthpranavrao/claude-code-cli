from functools import wraps
from time import sleep
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(attempts: int, retry_on: tuple[type[Exception], ...], delay: float = 0.01):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_error: Exception | None = None
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except retry_on as exc:
                    last_error = exc
                    if attempt < attempts - 1:
                        sleep(delay)
            assert last_error is not None
            raise last_error

        return wrapper

    return decorator

