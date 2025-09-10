import random
import time

def fixed_backoff(attempt, delay):
    """Always wait the same delay between retries."""
    time.sleep(delay)

def exponential_backoff(attempt, delay):
    """Wait with exponential growth: delay * 2^attempt."""
    wait_time = delay * (2 ** (attempt - 1))
    time.sleep(wait_time)

def jitter_backoff(attempt, delay):
    """Randomized wait to avoid thundering herd problem."""
    wait_time = delay + random.uniform(0, delay)
    time.sleep(wait_time)
