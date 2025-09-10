import random
import asyncio
from smart_retry import retry, RetryConditionError

print("=== SMART RETRY LIBRARY DEMO SCRIPT ===\n")

# -------------------------
# 1️⃣ Test basic retry on exceptions
# -------------------------
calls = {"count": 0}

@retry(times=3, delay=1)
def test_exception_retry():
    calls["count"] += 1
    print(f"[Exception Retry] Attempt {calls['count']}")
    if calls["count"] < 2:
        raise ValueError("Fail once")
    return "success"

result = test_exception_retry()
print("Result:", result, "\n")

# -------------------------
# 2️⃣ Test retry on condition
# -------------------------
calls_cond = {"count": 0}

@retry(times=4, delay=1, condition=lambda r: r == "ok")
def test_condition_retry():
    calls_cond["count"] += 1
    print(f"[Condition Retry] Attempt {calls_cond['count']}")
    return "fail"

try:
    test_condition_retry()
except RetryConditionError as e:
    print("Caught RetryConditionError:", e, "\n")

# -------------------------
# 3️⃣ Test backoff strategies
# -------------------------
print("Testing backoff strategies with simple function:")

@retry(times=3, delay=1, backoff="exponential")
def backoff_demo():
    print("Attempting with exponential backoff")
    raise ValueError("Demo fail")

try:
    backoff_demo()
except ValueError:
    print("Exponential backoff demo finished\n")

# -------------------------
# 4️⃣ Test logging to file
# -------------------------
@retry(times=3, delay=1, log_file="demo_retry.log")
def logging_demo():
    print("Logging demo attempt")
    raise ValueError("Fail for logging demo")

try:
    logging_demo()
except ValueError:
    print("Check 'demo_retry.log' for retry logs\n")

# -------------------------
# 5️⃣ Test async function retry
# -------------------------
async_calls = {"count": 0}

@retry(times=4, delay=1)
async def async_demo():
    async_calls["count"] += 1
    print(f"[Async Retry] Attempt {async_calls['count']}")
    if async_calls["count"] < 3:
        raise ValueError("Fail async")
    return "async success"

async def run_async_demo():
    result = await async_demo()
    print("Async Result:", result)

asyncio.run(run_async_demo())

print("\n=== DEMO COMPLETE ===")
