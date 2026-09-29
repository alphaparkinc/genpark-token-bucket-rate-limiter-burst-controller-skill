"""Token Bucket Rate Limiter with Burst Controller.
100% Python Standard Library.
"""

import time

class TokenBucketLimiter:
    """Token bucket rate limiter with burst capability for LLM token quotas."""
    def __init__(self, rate: float, capacity: float):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()

    def _refill(self, now: float = None):
        if now is None:
            now = time.time()
        elapsed = now - self.last_refill
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now

    def acquire(self, requested: float = 1.0, now: float = None) -> tuple:
        if now is None:
            now = time.time()
        self._refill(now)
        if self.tokens >= requested:
            self.tokens -= requested
            return True, 0.0
        else:
            deficit = requested - self.tokens
            wait_time = deficit / self.rate
            return False, round(wait_time, 4)

    def get_status(self) -> dict:
        self._refill()
        return {
            "rate_per_sec": self.rate,
            "capacity": self.capacity,
            "available_tokens": round(self.tokens, 2)
        }
