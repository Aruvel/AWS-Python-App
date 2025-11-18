# utils/decorators.py
# Path: utils/decorators.py
"""
Small utility decorators.
"""
import threading
from functools import wraps
from typing import Callable, Any


def run_in_thread(daemon: bool = True):
    """Decorator to run a function in a background thread (daemon by default)."""
    def deco(fn: Callable[..., Any]):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=daemon)
            t.start()
            return t
        return wrapper
    return deco


