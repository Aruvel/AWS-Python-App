# core/models.py
"""
Structured pydantic models for quiz questions & results
"""

from pydantic import BaseModel
from typing import List, Set


class Question(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answers: Set[int]
    explanation: str = ""
    topic: str = "General"
    difficulty: str = "Medium"


class QuizResult(BaseModel):
    score: int
    total: int
    percentage: float
    time_seconds: float
    is_exam: bool
