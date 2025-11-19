"""
Quiz Tab Interface
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Callable, Set
from datetime import datetime
from config.constants import EXAM_QUESTION_COUNT, PDF_EXTENSIONS
from ui.dialogs import ResultsDialog, ReviewWrongDialog


class QuizTab:
    """Quiz interface tab"""
    
    def __init__(self, parent, quiz_manager, config_manager, 
                 on_load_pdf: Callable, on_quiz_finished: Callable):
        self.parent = parent
        self.quiz_manager = quiz_manager
        self.config_manager = config_manager
        self.on_load_pdf = on_load_pdf
        self.on_quiz_finished = on_quiz_finished
        
        self.exam_timer_id = None
        self.selected_option = None
        self.selected_options = []
        
        self.create_ui()
    
    def create_ui(self):
        """Create quiz interface"""
        # Top controls
        self.create_top_controls()
        
        # Progress section
        self.create_progress_section()
        
        # Question display
        self.create_question_section()
        
        # Feedback section
        self.create_feedback_section()
        
        # Control buttons
        self.create_control_buttons()
    
    def create_top_controls(self):
        """Create top control bar"""
        top_frame = ctk.CTkFrame(self.parent)
        top_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        # PDF loader
        ctk.CTkButton(
            top_frame, 
            text="📁 Load PDF",
            command=self.load_pdf_dialog,
            width=120, 
            height=35
        ).pack(side="left", padx=(10, 20))
        
        # Quiz mode
        mode_frame = ctk.CTkFrame(top_frame)
        mode_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(mode_frame, text="Mode:").pack(side="left", padx=(10, 5))
        self.quiz_mode = tk.StringVar(value="Practice")
        self.mode_combo = ctk.CTkComboBox(
            mode_frame,
            values=["Practice", f"Exam ({EXAM_QUESTION_COUNT} Questions)"],
            variable=self.quiz_mode,
            width=180,
            command=self.on_mode_changed
        )
        self.mode_combo.pack(side="left", padx=(0, 10))
        
        # Question order
        order_frame = ctk.CTkFrame(top_frame)
        order_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(order_frame, text="Order:").pack(side="left", padx=(10, 5))
        default_order = self.config_manager.get("default_question_order", "Random")
        self.question_order = tk.StringVar(value=default_order)
        self.order_combo = ctk.CTkComboBox(
            order_frame,
            values=["Random", "Sequential (First to Last)", "Reverse (Last to First)"],
            variable=self.question_order,
            width=200
        )
        self.order_combo.pack(side="left", padx=(0, 10))
        
        # Difficulty filter
        self.filter_frame = ctk.CTkFrame(top_frame)
        self.filter_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(self.filter_frame, text="Difficulty:").pack(side="left", padx=(10, 5))
        self.difficulty_filter = tk.StringVar(value="All")
        self.difficulty_combo = ctk.CTkComboBox(
            self.filter_frame,
            values=["All", "Easy", "Medium", "Hard"],
            variable=self.difficulty_filter,
            width=100
        )
        self.difficulty_combo.pack(side="left", padx=(0, 10))
        
        # Start button
        control_frame = ctk.CTkFrame(top_frame)
        control_frame.pack(side="right", padx=10)
        
        self.start_button = ctk.CTkButton(
            control_frame,
            text="🚀 Start Quiz",
            command=self.start_quiz,
            width=120,
            height=35,
            state="disabled"
        )
        self.start_button.pack(side="left", padx=5)
    
    def create_progress_section(self):
        """Create progress display section"""
        progress_frame = ctk.CTkFrame(self.parent)
        progress_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        # Progress info
        info_frame = ctk.CTkFrame(progress_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        self.progress_label = ctk.CTkLabel(
            info_frame,
            text="No quiz loaded",
            font=("Arial", 14)
        )
        self.progress_label.pack(side="left")
        
        self.score_label = ctk.CTkLabel(
            info_frame,
            text="Score: 0/0",
            font=("Arial", 14, "bold")
        )
        self.score_label.pack(side="right")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
        self.progress_bar.pack(padx=10, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Timer
        self.timer_label = ctk.CTkLabel(progress_frame, text="", font=("Arial", 12))
        self.timer_label.pack(pady=5)
    
    def create_question_section(self):
        """Create question display section"""
        self.question_frame = ctk.CTkScrollableFrame(self.parent, height=300)
        self.question_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        self.question_label = ctk.CTkLabel(
            self.question_frame,
            text="Load a PDF to start the quiz",
            font=("Arial", 16),
            wraplength=800,
            justify="left"
        )
        self.question_label.pack(pady=20, padx=20)
        
        # Options container
        self.options_container = ctk.CTkFrame(self.question_frame)
        self.options_container.pack(fill="x", padx=20, pady=10)
    
    def create_feedback_section(self):
        """Create feedback display section"""
        self.feedback_frame = ctk.CTkFrame(self.parent)
        self.feedback_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        self.feedback_label = ctk.CTkLabel(
            self.feedback_frame,
            text="",
            font=("Arial", 14, "bold")
        )
        self.feedback_label.pack(pady=15)
    
    def create_control_buttons(self):
        """Create control buttons"""
        buttons_frame = ctk.CTkFrame(self.parent)
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Previous button
        self.prev_button = ctk.CTkButton(
            buttons_frame,
            text="← Previous",
            command=self.prev_question,
            width=100,
            height=40,
            state="disabled"
        )
        self.prev_button.pack(side="left", padx=5)
        
        # Submit button
        self.submit_button = ctk.CTkButton(
            buttons_frame,
            text="✓ Submit Answer",
            command=self.check_answer,
            width=150,
            height=40,
            state="disabled"
        )
        self.submit_button.pack(side="left", padx=5)
        
        # Next button
        self.next_button = ctk.CTkButton(
            buttons_frame,
            text="Next →",
            command=self.next_question,
            width=100,
            height=40,
            state="disabled"
        )
        self.next_button.pack(side="left", padx=5)
        
        # Hint button
        self.hint_button = ctk.CTkButton(
            buttons_frame,
            text="💡 Hint",
            command=self.show_hint,
            width=80,
            height=40,
            state="disabled"
        )
        self.hint_button.pack(side="left", padx=5)
        
        # Review buttons
        self.review_wrong_button = ctk.CTkButton(
            buttons_frame,
            text="📋 Review Wrong",
            command=self.show_review_wrong,
            width=150,
            height=40
        )
        self.review_wrong_button.pack(side="right", padx=(10, 5))
        
        self.review_all_button = ctk.CTkButton(
            buttons_frame,
            text="📖 Review All",
            command=self.show_review_all,
            width=130,
            height=40
        )
        self.review_all_button.pack(side="right", padx=5)
    
    def load_pdf_dialog(self):
        """Open file dialog to load PDF"""
        filename = filedialog.askopenfilename(
            title="Select AWS Quiz PDF",
            filetypes=PDF_EXTENSIONS
        )
        if filename:
            self.on_load_pdf(filename)
    
    def show_loading(self):
        """Show loading state"""
        self.question_label.configure(text="📚 Loading questions from PDF...")
        self.start_button.configure(state="disabled", text="Loading...")
    
    def on_questions_loaded(self, count):
        """Handle successful question loading"""
        self.question_label.configure(text=f"✅ Loaded {count} questions successfully!")
        self.start_button.configure(state="normal", text="🚀 Start Quiz")
    
    def on_questions_load_failed(self):
        """Handle failed question loading"""
        self.question_label.configure(text="❌ Failed to load questions from PDF")
        self.start_button.configure(state="disabled", text="No Questions")
    
    def on_mode_changed(self, *args):
        """Handle quiz mode change"""
        is_exam = "Exam" in self.quiz_mode.get()
        
        if is_exam:
            self.order_combo.configure(state="disabled")
            self.order_combo.set("Random")
            self.difficulty_combo.configure(state="disabled")
        else:
            self.order_combo.configure(state="normal")
            self.difficulty_combo.configure(state="normal")
    
    def start_quiz(self):
        """Start the quiz"""
        exam_mode = "Exam" in self.quiz_mode.get()
        difficulty = self.difficulty_filter.get()
        order = self.question_order.get()
        
        success = self.quiz_manager.start_quiz(
            exam_mode, 
            difficulty, 
            order,
            EXAM_QUESTION_COUNT
        )
        
        if not success:
            messagebox.showwarning(
                "Warning",
                f"Not enough questions for exam mode. Need {EXAM_QUESTION_COUNT}."
            )
            return
        
        # Update UI state
        if exam_mode:
            self.difficulty_combo.configure(state="disabled")
            self.hint_button.configure(state="disabled")
            self.start_exam_timer()
        else:
            self.hint_button.configure(state="normal")
        
        self.submit_button.configure(state="normal")
        self.load_question()
    
    def start_exam_timer(self):
        """Start exam countdown timer"""
        if self.exam_timer_id:
            self.parent.after_cancel(self.exam_timer_id)
        
        exam_time = self.config_manager.get("exam_time_limit", 90)
        self.quiz_manager.exam_time_remaining = exam_time * 60
        self.update_exam_timer()
    
    def update_exam_timer(self):
        """Update exam timer display"""
        if not self.quiz_manager.exam_mode or self.quiz_manager.exam_time_remaining <= 0:
            if self.quiz_manager.exam_mode and self.quiz_manager.exam_time_remaining <= 0:
                self.exam_timer_id = None
                messagebox.showwarning("Time's Up!", "Exam time limit reached!")
                self.finish_quiz()
            return
        
        remaining = self.quiz_manager.exam_time_remaining
        minutes = remaining // 60
        seconds = remaining % 60
        self.timer_label.configure(text=f"⏰ Time Remaining: {minutes:02d}:{seconds:02d}")
        
        # Color coding
        if minutes < 10:
            self.timer_label.configure(text_color="red")
        elif minutes < 20:
            self.timer_label.configure(text_color="orange")
        
        self.quiz_manager.exam_time_remaining -= 1
        self.exam_timer_id = self.parent.after(1000, self.update_exam_timer)
    
    def load_question(self):
        """Load current question"""
        question_data = self.quiz_manager.get_current_question()
        
        if not question_data:
            self.finish_quiz()
            return
        
        # Update progress
        total = len(self.quiz_manager.filtered_questions)
        current = self.quiz_manager.current_question_index + 1
        mode_text = "EXAM MODE" if self.quiz_manager.exam_mode else "Practice Mode"
        order_info = f"(#{question_data.get('id', 'N/A')})" if not self.quiz_manager.exam_mode else ""
        
        self.progress_label.configure(
            text=f"{mode_text} | Question {current} of {total} {order_info} | Topic: {question_data.get('topic', 'General')}"
        )
        self.progress_bar.set(current / total)
        
        # Clear previous options
        for widget in self.options_container.winfo_children():
            widget.destroy()
        
        # Display question
        question_display = f"Q{current}"
        if not self.quiz_manager.exam_mode and question_data.get('id'):
            question_display += f" (Original Q#{question_data['id']})"
        question_display += f": {question_data['question']}"
        
        self.question_label.configure(text=question_display)
        
        # Create answer options
        self.create_answer_options(question_data)
        
        # Update button states
        self.prev_button.configure(
            state="normal" if self.quiz_manager.current_question_index > 0 else "disabled"
        )
        self.submit_button.configure(state="normal", text="✓ Submit Answer")
        self.next_button.configure(state="disabled")
        self.next_button.configure(
            text="Finish Quiz" if current >= total else "Next →"
        )
        self.feedback_label.configure(text="")
        
        # Start question timer
        self.quiz_manager.question_start_time = datetime.now()
    
    def create_answer_options(self, question_data):
        """Create answer option widgets"""
        options = question_data['options']
        correct_answers = question_data['correct_answers']
        
        if len(correct_answers) == 1:
            # Single choice - radio buttons
            self.selected_option = tk.IntVar()
            for i, option_text in enumerate(options):
                radio = ctk.CTkRadioButton(
                    self.options_container,
                    text=f"{chr(65+i)}. {option_text}",
                    variable=self.selected_option,
                    value=i
                )
                radio.pack(anchor="w", padx=20, pady=5)
        else:
            # Multiple choice - checkboxes
            ctk.CTkLabel(
                self.options_container,
                text="Select ALL correct answers:",
                font=("Arial", 12, "italic")
            ).pack(anchor="w", padx=20, pady=5)
            
            self.selected_options = [tk.IntVar() for _ in options]
            for i, option_text in enumerate(options):
                checkbox = ctk.CTkCheckBox(
                    self.options_container,
                    text=f"{chr(65+i)}. {option_text}",
                    variable=self.selected_options[i]
                )
                checkbox.pack(anchor="w", padx=20, pady=5)
        
        # Restore previous answer if available
        self.restore_previous_answer(question_data)
    
    def restore_previous_answer(self, question_data):
        """Restore previously selected answer"""
        answered_q = next(
            (q for q in self.quiz_manager.answered_questions 
             if q["question"]["id"] == question_data["id"]),
            None
        )
        
        if answered_q:
            user_answers = answered_q["user_answer"]
            correct_answers = question_data['correct_answers']
            
            if len(correct_answers) == 1:
                if user_answers:
                    self.selected_option.set(list(user_answers)[0])
            else:
                for i, var in enumerate(self.selected_options):
                    var.set(1 if i in user_answers else 0)
    
    def get_user_answers(self) -> Set[int]:
        """Get user's selected answers"""
        question_data = self.quiz_manager.get_current_question()
        correct_answers = question_data['correct_answers']
        user_answers = set()
        
        if len(correct_answers) == 1:
            user_answers.add(self.selected_option.get())
        else:
            for i, var in enumerate(self.selected_options):
                if var.get():
                    user_answers.add(i)
        
        return user_answers
    
    def check_answer(self):
        """Check submitted answer"""
        if self.quiz_manager.answer_submitted:
            return
        
        user_answers = self.get_user_answers()
        result = self.quiz_manager.submit_answer(user_answers)
        
        if not result:
            return
        
        # Show feedback
        if result["is_correct"]:
            feedback_text = "🎉 Correct! Excellent work!"
            feedback_color = "green"
        else:
            correct_letters = [chr(65 + i) for i in sorted(result["correct_answers"])]
            feedback_text = f"❌ Incorrect! Correct answer(s): {', '.join(correct_letters)}"
            feedback_color = "red"
        
        # Show feedback (but not in exam mode)
        if not self.quiz_manager.exam_mode:
            self.feedback_label.configure(text=feedback_text, text_color=feedback_color)
            
            # Show explanation if available
            if not result["is_correct"] and self.config_manager.get("show_explanations"):
                if result["explanation"]:
                    explanation_text = f"💡 Explanation: {result['explanation']}"
                    self.feedback_label.configure(text=f"{feedback_text}\n{explanation_text}")
        else:
            self.feedback_label.configure(text="Answer recorded", text_color="blue")
        
        # Update score
        score = self.quiz_manager.score
        current = self.quiz_manager.current_question_index + 1
        self.score_label.configure(text=f"Score: {score}/{current}")
        
        # Update buttons
        self.submit_button.configure(state="disabled", text="Answer Submitted")
        self.next_button.configure(state="normal")
    
    def next_question(self):
        """Move to next question"""
        has_next = self.quiz_manager.next_question()
        if has_next:
            self.load_question()
        else:
            self.finish_quiz()
    
    def prev_question(self):
        """Move to previous question"""
        if self.quiz_manager.prev_question():
            self.load_question()
    
    def show_hint(self):
        """Show hint for current question"""
        eliminate = self.quiz_manager.get_hint()
        if eliminate is not None:
            messagebox.showinfo("💡 Hint", f"You can eliminate option {chr(65 + eliminate)}")
    
    def finish_quiz(self):
        """Finish the quiz"""
        # Stop exam timer
        if self.exam_timer_id:
            self.parent.after_cancel(self.exam_timer_id)
            self.exam_timer_id = None
            self.timer_label.configure(text="")
        
        # Re-enable controls
        if self.quiz_manager.exam_mode:
            self.difficulty_combo.configure(state="normal")
            self.hint_button.configure(state="normal")
            self.order_combo.configure(state="normal")
        
        # Get results
        results = self.quiz_manager.get_quiz_results()
        
        # Notify parent
        self.on_quiz_finished(results)
        
        # Show results dialog
        ResultsDialog(
            self.parent,
            results,
            self.quiz_manager.exam_mode,
            self.question_order.get(),
            self.on_retake_quiz,
            self.show_review_wrong,
            self.show_review_all
        )
    
    def on_retake_quiz(self):
        """Retake quiz"""
        self.start_quiz()
    
    def show_review_wrong(self):
        """Show review of wrong answers"""
        if not self.quiz_manager.wrong_answers:
            messagebox.showinfo("Review", "No wrong answers to review!")
            return
        
        ReviewWrongDialog(self.parent, self.quiz_manager.wrong_answers)
    
    def show_review_all(self):
        """Show review of all answers"""
        # This will switch to the review tab
        # Implementation depends on how tabs communicate
        pass
    
    def get_question_order(self) -> str:
        """Get current question order setting"""
        return self.question_order.get()