import sys
import json
from client import TokenBucketLimiter

limiter = TokenBucketLimiter(rate=100.0, capacity=200.0)

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-token-bucket-rate-limiter-burst-controller-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "acquire_tokens",
                        "description": "Attempts to acquire tokens from the bucket rate limiter",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "requested": {"type": "number", "default": 1.0}
                            }
                        }
                    },
                    {
                        "name": "get_status",
                        "description": "Returns current bucket fill level and rate capacity",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "acquire_tokens":
            ok, wait = limiter.acquire(args.get("requested", 1.0))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"allowed": ok, "wait_seconds": wait})}]}}
        elif name == "get_status":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(limiter.get_status())}]}}
            
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run()
