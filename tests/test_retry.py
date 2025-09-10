import pytest
from smart_retry import retry, RetryConditionError

def test_retry_success():
    calls = {"count": 0}
    @retry(times=3, delay=1)
    def test_func():
        calls["count"] += 1
        if calls["count"] < 2:
            raise ValueError("Fail once")
        return "success"
    assert test_func() == "success"

def test_retry_condition():
    calls = {"count": 0}
    @retry(times=2, delay=1, condition=lambda r: r == "ok")
    def test_func():
        calls["count"] += 1
        return "fail"
    with pytest.raises(RetryConditionError):
        test_func()
