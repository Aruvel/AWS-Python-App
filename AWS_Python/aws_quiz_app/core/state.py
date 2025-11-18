# core/state.py
"""
Centralized quiz state container — global but clean.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from core.models import Question


@dataclass
class QuizState:
    config: any
    questions: List[Question] = field(default_factory=list)
    filtered: List[Question] = field(default_factory=list)
    current_index: int = 0
    score: int = 0
    exam_mode: bool = False

    def reset(self):
        self.current_index = 0
        self.score = 0
