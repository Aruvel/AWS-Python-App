

# services/timer.py
# Path: services/timer.py
"""
Countdown timer utility for exam mode or per-question timers.
Runs on a background thread and calls callbacks on tick and finish.
"""
import threading
import time
from typing import Callable, Optional


class CountdownTimer:
    def __init__(self, seconds: int, tick_cb: Optional[Callable[[int], None]] = None, finish_cb: Optional[Callable[[], None]] = None):
        self._initial = int(seconds)
        self._remaining = int(seconds)
        self._tick_cb = tick_cb
        self._finish_cb = finish_cb
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self._remaining > 0 and not self._stop_event.is_set():
            time.sleep(1)
            self._remaining -= 1
            if callable(self._tick_cb):
                try:
                    self._tick_cb(self._remaining)
                except Exception:
                    pass
        if not self._stop_event.is_set():
            if callable(self._finish_cb):
                try:
                    self._finish_cb()
                except Exception:
                    pass

    def cancel(self):
        self._stop_event.set()
        self._remaining = self._initial

    def reset(self, seconds: Optional[int] = None):
        self.cancel()
        if seconds is not None:
            self._initial = int(seconds)
        self._remaining = int(self._initial)

    @property
    def remaining(self) -> int:
        return self._remaining

