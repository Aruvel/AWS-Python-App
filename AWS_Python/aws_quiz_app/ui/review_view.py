

# ui/review_view.py
"""
Review tab UI: shows answered questions with expandable details.
"""
import customtkinter as ctk
import tkinter as tk


class ReviewView:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.frame = parent
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self.frame)
        header.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(header, text="📋 Review", font=("Arial", 16, "bold")).pack(side="left", padx=8)

        self.mode_var = tk.StringVar(value="All")
        self.mode_combo = ctk.CTkComboBox(header, values=["All", "Correct", "Wrong"], variable=self.mode_var,
                                          command=lambda *_: self.refresh())
        self.mode_combo.pack(side="right", padx=8)

        self.content = ctk.CTkScrollableFrame(self.frame)
        self.content.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.empty_label = ctk.CTkLabel(self.content, text="Complete a quiz to see review items.", font=("Arial", 12))
        self.empty_label.pack(expand=True)

    def refresh(self):
        for w in self.content.winfo_children():
            w.destroy()

        answered = getattr(self.state, "answered_questions", [])
        if not answered:
            ctk.CTkLabel(self.content, text="No answered questions yet.", font=("Arial", 12)).pack(expand=True)
            return

        mode = self.mode_var.get()
        if mode == "Correct":
            filtered = [a for a in answered if a["is_correct"]]
        elif mode == "Wrong":
            filtered = [a for a in answered if not a["is_correct"]]
        else:
            filtered = answered

        for item in filtered:
            self._build_item(item)

    def _build_item(self, item):
        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="x", padx=8, pady=6)

        status = "✅" if item["is_correct"] else "❌"
        preview = item["question"].question
        header = ctk.CTkLabel(frame, text=f"{status} Q{item['question_number']}: {preview[:120]}",
                              cursor="hand2", wraplength=900)
        header.pack(fill="x", padx=8, pady=8)

        details = ctk.CTkFrame(frame)
        details.pack(fill="x", padx=8, pady=(0, 8))

        # options with colors
        correct_set = set(item["question"].correct_answers)
        user_set = set(item["user_answer"])

        for i, opt in enumerate(item["question"].options):
            row = ctk.CTkFrame(details)
            row.pack(fill="x", padx=6, pady=2)
            text = f"{chr(65+i)}. {opt}"
            if i in correct_set and i in user_set:
                # correct chosen
                row.configure(fg_color="green")
                ctk.CTkLabel(row, text=f"✅ {text}", text_color="white").pack(anchor="w", padx=8, pady=6)
            elif i in correct_set:
                row.configure(fg_color="#2a7b2a")
                ctk.CTkLabel(row, text=f"✓ {text}", text_color="white").pack(anchor="w", padx=8, pady=6)
            elif i in user_set:
                row.configure(fg_color="red")
                ctk.CTkLabel(row, text=f"✗ {text}", text_color="white").pack(anchor="w", padx=8, pady=6)
            else:
                ctk.CTkLabel(row, text=text).pack(anchor="w", padx=8, pady=6)

        # summary
        summ = ctk.CTkFrame(details)
        summ.pack(fill="x", padx=6, pady=(8, 6))
        ua = ", ".join(chr(65 + i) for i in sorted(user_set)) if user_set else "None"
        ca = ", ".join(chr(65 + i) for i in sorted(correct_set))
        ctk.CTkLabel(summ, text=f"Your answer: {ua}").pack(anchor="w", padx=6, pady=2)
        ctk.CTkLabel(summ, text=f"Correct answer: {ca}").pack(anchor="w", padx=6, pady=2)
        ctk.CTkLabel(summ, text=f"Time: {item.get('time_taken', 0):.1f} sec").pack(anchor="w", padx=6, pady=2)

