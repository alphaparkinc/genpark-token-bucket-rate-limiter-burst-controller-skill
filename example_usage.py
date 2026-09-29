from client import TokenBucketLimiter

limiter = TokenBucketLimiter(rate=50.0, capacity=100.0) # 50 tokens/sec
allowed, wait = limiter.acquire(40.0)
print("Request 40 tokens allowed:", allowed)
status = limiter.get_status()
print("Limiter status:", status)
