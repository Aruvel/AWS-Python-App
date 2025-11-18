# core/stats_manager.py
# Path: core/stats_manager.py
"""
Statistics manager: persistent storage and simple analytics for quizzes/exams.
Updates state.stats (a dict) and persists to a JSON file.
"""
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any
import csv


class StatsManager:
    def __init__(self, state, stats_file: str = "quiz_stats.json", max_quiz_history: int = 50, max_exam_history: int = 20):
        self.state = state
        self.stats_file = Path(stats_file)
        self.max_quiz_history = max_quiz_history
        self.max_exam_history = max_exam_history
        self.stats = self._load_stats()
        # attach to state for UI consumption
        setattr(self.state, "stats", self.stats)

    def _load_stats(self) -> Dict[str, Any]:
        if self.stats_file.exists():
            try:
                with open(self.stats_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        # default stats structure
        return {
            "total_quizzes": 0,
            "total_questions": 0,
            "correct_answers": 0,
            "average_score": 0.0,
            "best_score": 0.0,
            "quiz_history": [],
            "exam_history": [],
            "topic_performance": {},
            "difficulty_performance": {}
        }

    def _save(self):
        try:
            with open(self.stats_file, "w") as f:
                json.dump(self.stats, f, indent=2)
        except Exception:
            pass

    def _update_aggregate(self):
        tq = self.stats.get("total_questions", 0)
        ca = self.stats.get("correct_answers", 0)
        if tq > 0:
            self.stats["average_score"] = (ca / tq) * 100
        else:
            self.stats["average_score"] = 0.0

    def record_quiz(self, score: int, total: int, time_seconds: float, wrong_answers: int, is_exam: bool=False):
        """Record a completed quiz/exam and update aggregates."""
        percent = (score / total) * 100 if total else 0.0
        rec = {
            "date": datetime.now().isoformat(),
            "score": score,
            "total": total,
            "percentage": percent,
            "time": time_seconds,
            "wrong_answers": wrong_answers,
            "is_exam": bool(is_exam),
            "passed": (percent >= 70) if is_exam else (percent >= 80)
        }

        # update aggregates
        self.stats["total_quizzes"] = self.stats.get("total_quizzes", 0) + 1
        self.stats["total_questions"] = self.stats.get("total_questions", 0) + total
        self.stats["correct_answers"] = self.stats.get("correct_answers", 0) + score

        # best score
        if percent > self.stats.get("best_score", 0.0):
            self.stats["best_score"] = percent

        # append to appropriate history
        if is_exam:
            self.stats.setdefault("exam_history", []).append(rec)
            # trim
            self.stats["exam_history"] = self.stats["exam_history"][-self.max_exam_history:]
        else:
            self.stats.setdefault("quiz_history", []).append(rec)
            self.stats["quiz_history"] = self.stats["quiz_history"][-self.max_quiz_history:]

        self._update_aggregate()
        self._save()
        # ensure state.stats reference is fresh
        setattr(self.state, "stats", self.stats)
        return rec

    def export_csv(self, filename: str):
        """Export all history (quiz + exam) to CSV."""
        rows = (self.stats.get("quiz_history", []) + self.stats.get("exam_history", []))
        if not rows:
            raise ValueError("No history to export")
        keys = ["date", "score", "total", "percentage", "time", "wrong_answers", "is_exam", "passed"]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r.get(k, "") for k in keys})

    def get_recent_history(self, limit: int = 20):
        """Return combined recent history (sorted by date)."""
        all_hist = (self.stats.get("quiz_history", []) + self.stats.get("exam_history", []))
        try:
            all_hist_sorted = sorted(all_hist, key=lambda x: x["date"])
        except Exception:
            all_hist_sorted = all_hist
        return all_hist_sorted[-limit:]
