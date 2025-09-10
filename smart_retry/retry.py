import functools
import inspect
from .backoff import fixed_backoff, exponential_backoff, jitter_backoff
from .logger import get_logger

class RetryConditionError(Exception):
    """Custom exception raised when retry condition not met."""
    pass

def retry(times=3, delay=1, backoff="fixed", 
          exceptions=(Exception,), condition=None, 
          log_file=None, log=True):
    """
    Retry decorator.
    
    Args:
        times (int): Max number of attempts.
        delay (int): Base delay between attempts.
        backoff (str): "fixed", "exponential", or "jitter".
        exceptions (tuple): Exceptions that trigger retry.
        condition (callable): A function that returns True when retry needed.
        log_file (str): File path for logging (default None = console).
        log (bool): Enable/disable logging.
    """
    backoff_map = {
        "fixed": fixed_backoff,
        "exponential": exponential_backoff,
        "jitter": jitter_backoff
    }

    def decorator(func):
        is_async = inspect.iscoroutinefunction(func)
        logger = get_logger(log_file) if log else None

        if is_async:
            async def wrapper(*args, **kwargs):
                for attempt in range(1, times + 1):
                    try:
                        result = await func(*args, **kwargs)

                        if condition and not condition(result):
                            raise RetryConditionError("Condition not met")

                        if logger:
                            logger.info(f"Attempt {attempt} SUCCESS ✅")
                        return result

                    except exceptions as e:
                        if attempt == times:
                            if logger:
                                logger.error(f"Final attempt {attempt} FAILED ❌: {e}")
                            raise
                        if logger:
                            logger.warning(f"Attempt {attempt} FAILED: {e}")
                        backoff_map[backoff](attempt, delay)
            return functools.wraps(func)(wrapper)

        else:
            def wrapper(*args, **kwargs):
                for attempt in range(1, times + 1):
                    try:
                        result = func(*args, **kwargs)

                        if condition and not condition(result):
                            raise RetryConditionError("Condition not met")

                        if logger:
                            logger.info(f"Attempt {attempt} SUCCESS ✅")
                        return result

                    except exceptions as e:
                        if attempt == times:
                            if logger:
                                logger.error(f"Final attempt {attempt} FAILED ❌: {e}")
                            raise
                        if logger:
                            logger.warning(f"Attempt {attempt} FAILED: {e}")
                        backoff_map[backoff](attempt, delay)
            return functools.wraps(func)(wrapper)

    return decorator
