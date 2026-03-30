from fastapi import Request

def rate_limit(request: Request):
    """
    Dummy rate limiter dependency.
    In a real production app, use Redis to limit requests per IP/user.
    """
    pass
