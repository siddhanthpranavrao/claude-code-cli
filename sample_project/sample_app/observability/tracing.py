from contextlib import contextmanager
from time import perf_counter

from sample_app.observability.logger import get_logger

logger = get_logger(__name__)


@contextmanager
def trace_span(name: str):
    started = perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (perf_counter() - started) * 1000
        logger.info("trace span completed", extra={"span": name, "elapsed_ms": elapsed_ms})

