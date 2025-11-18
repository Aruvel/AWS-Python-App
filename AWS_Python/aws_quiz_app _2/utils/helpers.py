# utils/helpers.py
# Path: utils/helpers.py
"""
Small helper utilities.
"""
import traceback
from typing import Callable, Any


def safe_call(fn: Callable[..., Any], *args, **kwargs):
    """Call fn safely, return (result, None) or (None, exception_str)."""
    try:
        return fn(*args, **kwargs), None
    except Exception as e:
        return None, traceback.format_exc()
