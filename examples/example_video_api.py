from smart_retry import retry, RetryConditionError
import random

# Fake API call simulation
def fake_get_video(video_id):
    if random.random() < 0.7:  # 70% chance it's "not ready"
        raise RetryConditionError("Video still processing...")
    return {"video_id": video_id, "status": "ready"}

@retry(times=5, delay=2, backoff="exponential", 
       condition=lambda r: r.get("status") == "ready",
       log_file="retry_logs.txt")
def poll_video(video_id):
    return fake_get_video(video_id)

if __name__ == "__main__":
    print(poll_video("abcd1234"))
