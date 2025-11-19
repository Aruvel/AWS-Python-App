"""
Dialog Windows
"""

import tkinter as tk
import customtkinter as ctk
from typing import Callable, List, Dict
from config.constants import EXAM_PASSING_SCORE, EMOJI


class ResultsDialog:
    """Quiz results dialog"""
    
    def __init__(self, parent, results: Dict, is_exam: bool, question_order: str,
                 on_retake: Callable, on_review_wrong: Callable, on_review_all: Callable):
        self.results = results
        self.is_exam = is_exam
        self.question_order = question_order
        self.on_retake = on_retake
        self.on_review_wrong = on_review_wrong
        self.on_review_all = on_review_all
        
        self.create_dialog(parent)
    
    def create_dialog(self, parent):
        """Create results dialog window"""
        window = ctk.CTkToplevel(parent)
        window.title("🏆 Quiz Results")
        window.geometry("700x600")
        window.transient(parent)
        window.grab_set()
        
        main_frame = ctk.CTkFrame(window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_text = "🏆 Exam Complete!" if self.is_exam else "🏆 Quiz Complete!"
        ctk.CTkLabel(
            main_frame,
            text=title_text,
            font=("Arial", 24, "bold")
        ).pack(pady=(20, 30))
        
        # Score
        percentage = self.results["percentage"]
        ctk.CTkLabel(
            main_frame,
            text=f"Final Score: {self.results['score']}/{self.results['total']} ({percentage:.1f}%)",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        # Performance message
        performance, color = self.get_performance_message(percentage)
        ctk.CTkLabel(
            main_frame,
            text=performance,
            font=("Arial", 14),
            text_color=color
        ).pack(pady=10)
        
        # Statistics
        self.create_statistics_section(main_frame)
        
        # Buttons
        self.create_button_section(main_frame, window)
    
    def get_performance_message(self, percentage):
        """Get performance message and color"""
        if self.is_exam:
            if percentage >= EXAM_PASSING_SCORE:
                return "🎉 PASSED! Congratulations on passing the exam!", "green"
            else:
                return f"📚 Not quite there. You need {EXAM_PASSING_SCORE}% to pass (got {percentage:.1f}%)", "red"
        else:
            if percentage >= 90:
                return "🌟 Outstanding! You're ready for the exam!", "green"
            elif percentage >= 80:
                return "🎯 Excellent work! Just a bit more practice.", "blue"
            elif percentage >= 70:
                return "👍 Good job! Keep studying those weak areas.", "orange"
            elif percentage >= 60:
                return "📚 Not bad, but more study time needed.", "orange"
            else:
                return "💪 Keep practicing! You'll get there!", "red"
    
    def create_statistics_section(self, parent):
        """Create statistics display section"""
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        stats_title = "Exam Statistics:" if self.is_exam else "Quiz Statistics:"
        ctk.CTkLabel(
            stats_frame,
            text=stats_title,
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Total Time: {self.results['total_time']/60:.1f} minutes"
        ).pack(pady=2)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Average Time per Question: {self.results['avg_time']:.1f} seconds"
        ).pack(pady=2)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Correct Answers: {self.results['score']}"
        ).pack(pady=2)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Wrong Answers: {self.results['wrong_count']}"
        ).pack(pady=2)
        
        if self.is_exam:
            ctk.CTkLabel(
                stats_frame,
                text=f"Passing Score Required: {EXAM_PASSING_SCORE}% (46/65)",
                font=("Arial", 11, "italic")
            ).pack(pady=2)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Question Order: {self.question_order}",
            font=("Arial", 11)
        ).pack(pady=2)
    
    def create_button_section(self, parent, window):
        """Create button section"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        retake_text = "Retake Exam" if self.is_exam else "Take Again"
        ctk.CTkButton(
            button_frame,
            text=retake_text,
            command=lambda: [window.destroy(), self.on_retake()],
            width=140
        ).pack(side="left", padx=10)
        
        if self.results['wrong_count'] > 0:
            ctk.CTkButton(
                button_frame,
                text="Review Wrong",
                command=lambda: [window.destroy(), self.on_review_wrong()],
                width=140
            ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Review All",
            command=lambda: [window.destroy(), self.on_review_all()],
            width=120
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Close",
            command=window.destroy,
            width=100
        ).pack(side="right", padx=10)


class ReviewWrongDialog:
    """Review wrong answers dialog"""
    
    def __init__(self, parent, wrong_answers: List[Dict]):
        self.wrong_answers = wrong_answers
        self.create_dialog(parent)
    
    def create_dialog(self, parent):
        """Create review dialog window"""
        window = ctk.CTkToplevel(parent)
        window.title("📋 Review Wrong Answers")
        window.geometry("900x700")
        window.transient(parent)
        
        # Header
        header_frame = ctk.CTkFrame(window)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="📋 Wrong Answers Review",
            font=("Arial", 18, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_frame,
            text=f"Total: {len(self.wrong_answers)} questions",
            font=("Arial", 12)
        ).pack(side="right")
        
        # Question selector
        selector_frame = ctk.CTkFrame(window)
        selector_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(selector_frame, text="Select Question:").pack(side="left", padx=10)
        
        # Create dropdown options
        dropdown_options = []
        for wrong in self.wrong_answers:
            question_preview = wrong["question"]["question"][:60]
            if len(wrong["question"]["question"]) > 60:
                question_preview += "..."
            dropdown_options.append(f"Q{wrong['question_number']}: {question_preview}")
        
        selected_question = tk.StringVar()
        
        # Content frame
        content_frame = ctk.CTkScrollableFrame(window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        question_dropdown = ctk.CTkComboBox(
            selector_frame,
            values=dropdown_options,
            variable=selected_question,
            width=500,
            command=lambda choice: self.show_selected_question(choice, content_frame)
        )
        question_dropdown.pack(side="left", padx=10, fill="x", expand=True)
        
        # Show first question by default
        if dropdown_options:
            question_dropdown.set(dropdown_options[0])
            self.show_selected_question(dropdown_options[0], content_frame)
    
    def show_selected_question(self, selection, content_frame):
        """Show selected wrong question"""
        if not selection:
            return
        
        # Clear content
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        # Extract question number
        question_num = int(selection.split(":")[0][1:])
        
        # Find question
        wrong_answer = next(
            (w for w in self.wrong_answers if w["question_number"] == question_num),
            None
        )
        
        if not wrong_answer:
            return
        
        question_data = wrong_answer["question"]
        user_answers = wrong_answer["user_answer"]
        correct_answers = set(question_data["correct_answers"])
        
        # Question frame
        question_frame = ctk.CTkFrame(content_frame)
        question_frame.pack(fill="x", pady=10)
        
        # Question text
        ctk.CTkLabel(
            question_frame,
            text=f"Question {question_num}: {question_data['question']}",
            font=("Arial", 14, "bold"),
            wraplength=800,
            justify="left"
        ).pack(padx=15, pady=15, anchor="w")
        
        # Options with highlighting
        options_frame = ctk.CTkFrame(question_frame)
        options_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for i, option_text in enumerate(question_data["options"]):
            option_frame = ctk.CTkFrame(options_frame)
            option_frame.pack(fill="x", pady=2)
            
            # Determine styling
            if i in correct_answers:
                option_color = "green"
                prefix = "✓ "
                font_weight = "bold"
            elif i in user_answers:
                option_color = "red"
                prefix = "✗ "
                font_weight = "normal"
            else:
                option_color = "transparent"
                prefix = "  "
                font_weight = "normal"
            
            if option_color != "transparent":
                option_frame.configure(fg_color=option_color, corner_radius=5)
            
            ctk.CTkLabel(
                option_frame,
                text=f"{prefix}{chr(65+i)}. {option_text}",
                font=("Arial", 12, font_weight),
                wraplength=750
            ).pack(padx=10, pady=8, anchor="w")
        
        # Answer summary
        summary_frame = ctk.CTkFrame(content_frame)
        summary_frame.pack(fill="x", pady=10)
        
        user_answer_letters = [chr(65 + i) for i in sorted(user_answers)]
        correct_answer_letters = [chr(65 + i) for i in sorted(correct_answers)]
        
        ctk.CTkLabel(
            summary_frame,
            text=f"Your Answer: {', '.join(user_answer_letters) if user_answer_letters else 'None'}",
            font=("Arial", 12),
            text_color="red"
        ).pack(padx=15, pady=5, anchor="w")
        
        ctk.CTkLabel(
            summary_frame,
            text=f"Correct Answer: {', '.join(correct_answer_letters)}",
            font=("Arial", 12, "bold"),
            text_color="green"
        ).pack(padx=15, pady=5, anchor="w")
        
        # Explanation
        if question_data.get('explanation'):
            explanation_frame = ctk.CTkFrame(content_frame)
            explanation_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(
                explanation_frame,
                text="💡 Explanation:",
                font=("Arial", 12, "bold")
            ).pack(padx=15, pady=(10, 5), anchor="w")
            
            ctk.CTkLabel(
                explanation_frame,
                text=question_data['explanation'],
                font=("Arial", 11),
                wraplength=800,
                justify="left"
            ).pack(padx=15, pady=(0, 10), anchor="w")