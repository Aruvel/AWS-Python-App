"""
Review Tab Interface
"""

import tkinter as tk
import customtkinter as ctk


class ReviewTab:
    """Review interface tab"""
    
    def __init__(self, parent, quiz_manager):
        self.parent = parent
        self.quiz_manager = quiz_manager
        
        self.create_ui()
    
    def create_ui(self):
        """Create review interface"""
        # Controls
        controls = ctk.CTkFrame(self.parent)
        controls.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            controls,
            text="📋 Question Review",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=10)
        
        # Review mode selector
        self.review_mode = tk.StringVar(value="All Questions")
        review_mode_combo = ctk.CTkComboBox(
            controls,
            values=["All Questions", "Wrong Answers Only", "Correct Answers Only"],
            variable=self.review_mode,
            width=180,
            command=self.update_display
        )
        review_mode_combo.pack(side="right", padx=10)
        
        # Content frame
        self.review_content = ctk.CTkScrollableFrame(self.parent)
        self.review_content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial message
        self.show_empty_message()
    
    def show_empty_message(self):
        """Show empty state message"""
        for widget in self.review_content.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.review_content,
            text="Complete a quiz to review questions",
            font=("Arial", 14)
        ).pack(expand=True)
    
    def update_display(self, *args):
        """Update review display"""
        # Clear existing content
        for widget in self.review_content.winfo_children():
            widget.destroy()
        
        if not self.quiz_manager.answered_questions:
            self.show_empty_message()
            return
        
        # Filter questions
        review_mode = self.review_mode.get()
        if review_mode == "Wrong Answers Only":
            questions_to_show = [q for q in self.quiz_manager.answered_questions 
                               if not q["is_correct"]]
        elif review_mode == "Correct Answers Only":
            questions_to_show = [q for q in self.quiz_manager.answered_questions 
                               if q["is_correct"]]
        else:
            questions_to_show = self.quiz_manager.answered_questions
        
        if not questions_to_show:
            ctk.CTkLabel(
                self.review_content,
                text=f"No questions to show for '{review_mode}'",
                font=("Arial", 14)
            ).pack(expand=True)
            return
        
        # Header
        header_frame = ctk.CTkFrame(self.review_content)
        header_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"Showing {len(questions_to_show)} questions ({review_mode})",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Show questions
        for i, answered_q in enumerate(questions_to_show):
            self.create_question_review(answered_q, i)
    
    def create_question_review(self, answered_q, index):
        """Create collapsible question review item"""
        question_data = answered_q["question"]
        is_correct = answered_q["is_correct"]
        
        # Main frame
        main_frame = ctk.CTkFrame(self.review_content)
        main_frame.pack(fill="x", padx=10, pady=5)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        status_icon = "✅" if is_correct else "❌"
        question_preview = question_data["question"][:100]
        if len(question_data["question"]) > 100:
            question_preview += "..."
        
        header_text = f"{status_icon} Q{answered_q['question_number']}: {question_preview}"
        header_label = ctk.CTkLabel(
            header_frame,
            text=header_text,
            font=("Arial", 12),
            wraplength=800,
            justify="left",
            cursor="hand2"
        )
        header_label.pack(anchor="w")
        
        # Details frame (initially hidden)
        details_frame = ctk.CTkFrame(main_frame)
        details_visible = tk.BooleanVar(value=False)
        
        def toggle_details():
            if details_visible.get():
                details_frame.pack_forget()
                details_visible.set(False)
            else:
                details_frame.pack(fill="x", padx=10, pady=(0, 10))
                details_visible.set(True)
                
                if not details_frame.winfo_children():
                    self.populate_question_details(details_frame, answered_q)
        
        header_label.bind("<Button-1>", lambda e: toggle_details())
    
    def populate_question_details(self, details_frame, answered_q):
        """Populate question details"""
        question_data = answered_q["question"]
        user_answers = answered_q["user_answer"]
        correct_answers = set(question_data["correct_answers"])
        
        # Full question
        ctk.CTkLabel(
            details_frame,
            text=f"Full Question: {question_data['question']}",
            font=("Arial", 12, "bold"),
            wraplength=750,
            justify="left"
        ).pack(padx=10, pady=(10, 15), anchor="w")
        
        # Options with highlighting
        for i, option_text in enumerate(question_data["options"]):
            option_frame = ctk.CTkFrame(details_frame)
            option_frame.pack(fill="x", padx=10, pady=2)
            
            # Styling
            if i in correct_answers and i in user_answers:
                bg_color = "green"
                prefix = "✅ "
                text_color = "white"
            elif i in correct_answers:
                bg_color = "darkgreen"
                prefix = "✓ "
                text_color = "white"
            elif i in user_answers:
                bg_color = "red"
                prefix = "❌ "
                text_color = "white"
            else:
                bg_color = "transparent"
                prefix = "   "
                text_color = None
            
            if bg_color != "transparent":
                option_frame.configure(fg_color=bg_color)
            
            label_kwargs = {
                "text": f"{prefix}{chr(65+i)}. {option_text}",
                "font": ("Arial", 11),
                "wraplength": 700
            }
            if text_color:
                label_kwargs["text_color"] = text_color
            
            ctk.CTkLabel(option_frame, **label_kwargs).pack(padx=10, pady=5, anchor="w")
        
        # Summary
        summary_frame = ctk.CTkFrame(details_frame)
        summary_frame.pack(fill="x", padx=10, pady=10)
        
        user_answer_letters = [chr(65 + i) for i in sorted(user_answers)]
        correct_answer_letters = [chr(65 + i) for i in sorted(correct_answers)]
        
        ctk.CTkLabel(
            summary_frame,
            text=f"Your Answer: {', '.join(user_answer_letters) if user_answer_letters else 'None'}",
            font=("Arial", 11)
        ).pack(padx=10, pady=2, anchor="w")
        
        ctk.CTkLabel(
            summary_frame,
            text=f"Correct Answer: {', '.join(correct_answer_letters)}",
            font=("Arial", 11, "bold"),
            text_color="green"
        ).pack(padx=10, pady=2, anchor="w")
        
        ctk.CTkLabel(
            summary_frame,
            text=f"Time Taken: {answered_q['time_taken']:.1f} seconds",
            font=("Arial", 10)
        ).pack(padx=10, pady=2, anchor="w")
        
        # Explanation
        if question_data.get('explanation'):
            exp_frame = ctk.CTkFrame(details_frame)
            exp_frame.pack(fill="x", padx=10, pady=(5, 10))
            
            ctk.CTkLabel(
                exp_frame,
                text="💡 Explanation:",
                font=("Arial", 11, "bold")
            ).pack(padx=10, pady=(8, 2), anchor="w")
            
            ctk.CTkLabel(
                exp_frame,
                text=question_data['explanation'],
                font=("Arial", 10),
                wraplength=700,
                justify="left"
            ).pack(padx=10, pady=(0, 8), anchor="w")