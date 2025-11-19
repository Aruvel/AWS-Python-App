"""
Statistics Management
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime


class StatisticsManager:
    """Manages quiz statistics"""
    
    DEFAULT_STATS = {
        "total_quizzes": 0,
        "total_questions": 0,
        "correct_answers": 0,
        "average_score": 0,
        "best_score": 0,
        "quiz_history": [],
        "exam_history": [],
        "topic_performance": {},
        "difficulty_performance": {}
    }
    
    def __init__(self, stats_file: str):
        self.stats_file = stats_file
        self.stats = self.load()
    
    def load(self) -> Dict:
        """Load statistics from file"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return {**self.DEFAULT_STATS, **json.load(f)}
            else:
                return self.DEFAULT_STATS.copy()
        except Exception as e:
            print(f"Error loading statistics: {e}")
            return self.DEFAULT_STATS.copy()
    
    def save(self) -> bool:
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving statistics: {e}")
            return False
    
    def record_quiz(self, results: Dict, question_order: str) -> None:
        """Record quiz results"""
        self.stats["total_quizzes"] += 1
        self.stats["total_questions"] += results["total"]
        self.stats["correct_answers"] += results["score"]
        
        # Calculate averages
        if self.stats["total_questions"] > 0:
            self.stats["average_score"] = (
                self.stats["correct_answers"] / self.stats["total_questions"]
            ) * 100
        
        # Update best score
        if results["percentage"] > self.stats.get("best_score", 0):
            self.stats["best_score"] = results["percentage"]
        
        # Create quiz record
        passing_score = 70 if results["is_exam"] else 80
        quiz_record = {
            "date": datetime.now().isoformat(),
            "score": results["score"],
            "total": results["total"],
            "percentage": results["percentage"],
            "time": results["total_time"],
            "wrong_answers": results["wrong_count"],
            "is_exam": results["is_exam"],
            "passed": results["percentage"] >= passing_score,
            "question_order": question_order
        }
        
        # Add to appropriate history
        if results["is_exam"]:
            if "exam_history" not in self.stats:
                self.stats["exam_history"] = []
            self.stats["exam_history"].append(quiz_record)
            self.stats["exam_history"] = self.stats["exam_history"][-20:]
        else:
            if "quiz_history" not in self.stats:
                self.stats["quiz_history"] = []
            self.stats["quiz_history"].append(quiz_record)
            self.stats["quiz_history"] = self.stats["quiz_history"][-50:]
        
        self.save()
    
    def get_summary(self) -> Dict:
        """Get statistics summary"""
        return {
            "total_quizzes": self.stats.get("total_quizzes", 0),
            "average_score": self.stats.get("average_score", 0),
            "best_score": self.stats.get("best_score", 0),
            "exam_attempts": len(self.stats.get("exam_history", []))
        }
    
    def get_history(self, exam_only: bool = False) -> List[Dict]:
        """Get quiz history"""
        if exam_only:
            return self.stats.get("exam_history", [])
        return self.stats.get("quiz_history", []) + self.stats.get("exam_history", [])
    
    def reset(self) -> None:
        """Reset all statistics"""
        self.stats = self.DEFAULT_STATS.copy()
        self.save()