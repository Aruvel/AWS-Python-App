# services/quiz_engine.py
"""
Quiz engine: filtering, randomization, scoring
"""

import random
from core.state import QuizState
from core.models import Question


class QuizEngine:
    def __init__(self, state: QuizState, config):
        self.state = state
        self.config = config

    def load_questions(self, questions: list[Question]):
        self.state.questions = questions

    def apply_filters(self, difficulty="All"):
        if difficulty == "All":
            self.state.filtered = list(self.state.questions)
        else:
            self.state.filtered = [
                q for q in self.state.questions if q.difficulty == difficulty
            ]

        if self.config.randomize_questions:
            random.shuffle(self.state.filtered)

    def start_exam_mode(self, count=65):
        self.state.exam_mode = True
        self.state.filtered = random.sample(self.state.questions, count)
        self.state.current_index = 0
        self.state.score = 0

    def submit_answer(self, user_indices: set[int]):
        q = self.state.filtered[self.state.current_index]
        correct = q.correct_answers
        if user_indices == correct:
            self.state.score += 1
            return True
        return False

    def next_question(self):
        self.state.current_index += 1
        return self.state.current_index < len(self.state.filtered)
