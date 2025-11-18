# core/config.py
"""
Application configuration (loaded/stored from JSON)
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class AppConfig:
    randomize_questions: bool = True
    show_explanations: bool = True
    timer_enabled: bool = False
    time_per_question: int = 90
    exam_time_limit: int = 90
    theme: str = "dark"

    @staticmethod
    def load(path: str) -> "AppConfig":
        file = Path(path)
        if not file.exists():
            config = AppConfig()
            config.save(path)
            return config

        with open(path) as f:
            raw = json.load(f)
        return AppConfig(**raw)

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)
