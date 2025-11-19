"""
Quiz Manager - Handles quiz logic and state
"""

import random
from typing import List, Dict, Set, Optional
from datetime import datetime


class QuizManager:
    """Manages quiz state and logic"""
    
    def __init__(self):
        self.all_questions = []
        self.filtered_questions = []
        self.current_question_index = 0
        self.score = 0
        self.answer_submitted = False
        self.start_time = None
        self.question_start_time = None
        self.question_times = []
        self.wrong_answers = []
        self.answered_questions = []
        self.exam_mode = False
        self.exam_time_remaining = 0
    
    def load_questions(self, questions: List[Dict]) -> None:
        """Load questions into the manager"""
        self.all_questions = questions
        self.filtered_questions = questions.copy()
    
    def start_quiz(self, exam_mode: bool, difficulty_filter: str, 
                   question_order: str, exam_question_count: int = 65) -> bool:
        """Start a new quiz"""
        if not self.all_questions:
            return False
        
        self.exam_mode = exam_mode
        
        # Select questions
        if exam_mode:
            if len(self.all_questions) < exam_question_count:
                return False
            self.filtered_questions = random.sample(self.all_questions, exam_question_count)
        else:
            self.apply_filters(difficulty_filter)
        
        # Apply ordering
        self.apply_question_order(question_order)
        
        # Reset state
        self.current_question_index = 0
        self.score = 0
        self.answer_submitted = False
        self.start_time = datetime.now()
        self.question_times = []
        self.wrong_answers = []
        self.answered_questions = []
        
        return True
    
    def apply_filters(self, difficulty_filter: str) -> None:
        """Apply difficulty filter"""
        filtered = self.all_questions.copy()
        
        if difficulty_filter != "All":
            filtered = [q for q in filtered if q["difficulty"] == difficulty_filter]
        
        self.filtered_questions = filtered
    
    def apply_question_order(self, order: str) -> None:
        """Apply question ordering"""
        if order == "Random":
            random.shuffle(self.filtered_questions)
        elif order == "Sequential (First to Last)":
            self.filtered_questions.sort(key=lambda q: q.get("id", 0))
        elif order == "Reverse (Last to First)":
            self.filtered_questions.sort(key=lambda q: q.get("id", 0), reverse=True)
    
    def get_current_question(self) -> Optional[Dict]:
        """Get current question"""
        if self.current_question_index < len(self.filtered_questions):
            return self.filtered_questions[self.current_question_index]
        return None
    
    def submit_answer(self, user_answers: Set[int]) -> Dict:
        """Submit and check answer"""
        if self.answer_submitted:
            return None
        
        question_data = self.get_current_question()
        if not question_data:
            return None
        
        correct_answers = set(question_data['correct_answers'])
        is_correct = user_answers == correct_answers
        
        # Record timing
        question_time = (datetime.now() - self.question_start_time).total_seconds()
        self.question_times.append(question_time)
        
        # Update statistics
        question_data['times_answered'] += 1
        if is_correct:
            self.score += 1
            question_data['times_correct'] += 1
        
        # Store answered question
        answered_question = {
            "question": question_data,
            "user_answer": user_answers,
            "is_correct": is_correct,
            "question_number": self.current_question_index + 1,
            "time_taken": question_time
        }
        self.answered_questions.append(answered_question)
        
        if not is_correct:
            self.wrong_answers.append(answered_question)
        
        self.answer_submitted = True
        
        return {
            "is_correct": is_correct,
            "correct_answers": correct_answers,
            "explanation": question_data.get('explanation', ''),
            "time_taken": question_time
        }
    
    def next_question(self) -> bool:
        """Move to next question"""
        self.current_question_index += 1
        self.answer_submitted = False
        self.question_start_time = datetime.now()
        return self.current_question_index < len(self.filtered_questions)
    
    def prev_question(self) -> bool:
        """Move to previous question"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.answer_submitted = False
            return True
        return False
    
    def get_quiz_results(self) -> Dict:
        """Get quiz results"""
        total_time = (datetime.now() - self.start_time).total_seconds()
        total_questions = len(self.filtered_questions)
        percentage = (self.score / total_questions) * 100 if total_questions > 0 else 0
        
        return {
            "score": self.score,
            "total": total_questions,
            "percentage": percentage,
            "total_time": total_time,
            "avg_time": sum(self.question_times) / len(self.question_times) if self.question_times else 0,
            "wrong_count": len(self.wrong_answers),
            "is_exam": self.exam_mode
        }
    
    def get_hint(self) -> Optional[int]:
        """Get hint by eliminating one wrong answer"""
        if self.answer_submitted or self.exam_mode:
            return None
        
        question_data = self.get_current_question()
        if not question_data:
            return None
        
        correct_answers = set(question_data['correct_answers'])
        
        # Single choice only
        if len(correct_answers) != 1:
            return None
        
        wrong_options = [i for i in range(len(question_data['options'])) 
                        if i not in correct_answers]
        
        if wrong_options:
            return random.choice(wrong_options)
        
        return None