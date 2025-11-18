# utils/hashing.py
# Path: utils/hashing.py
"""
Hashing utility for file caching.
"""
import hashlib


def file_md5_short(path: str, length: int = 8) -> str:
    """Return first `length` chars of md5 for file at path."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()[:length]


