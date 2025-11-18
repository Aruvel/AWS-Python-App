# ui/review_view.py
import customtkinter as ctk
import tkinter as tk
from ui.widgets.collapsible_panel import CollapsiblePanel


class ReviewView:
    def __init__(self, parent, state):
        self.frame = parent
        self.state = state
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self.frame)
        top.pack(fill="x", pady=10)

        self.mode_var = tk.StringVar(value="All")
        self.mode_box = ctk.CTkComboBox(top, values=["All", "Correct", "Wrong"], variable=self.mode_var,
                                        command=lambda *_: self.refresh())
        self.mode_box.pack(side="right", padx=10)

        self.area = ctk.CTkScrollableFrame(self.frame)
        self.area.pack(fill="both", expand=True, pady=10)

    def refresh(self):
        for w in self.area.winfo_children():
            w.destroy()

        items = self.state.answered_questions

        mode = self.mode_var.get()
        if mode == "Correct":
            items = [x for x in items if x["is_correct"]]
        elif mode == "Wrong":
            items = [x for x in items if not x["is_correct"]]

        for rec in items:
            panel = CollapsiblePanel(self.area, title=f"Q{rec['question_number']} {'✔' if rec['is_correct'] else '✘'}",
                                     open_by_default=False)
            panel.pack(fill="x", pady=6, padx=10)

            q = rec["question"]
            detail = ctk.CTkLabel(panel.body, text=f"Q: {q.question}", wraplength=900, justify="left")
            detail.pack(fill="x", padx=6, pady=4)

            ua = ", ".join(chr(65+i) for i in sorted(rec["user_answer"]))
            ca = ", ".join(chr(65+i) for i in sorted(q.correct_answers))
            ctk.CTkLabel(panel.body, text=f"Your answer: {ua}").pack(anchor="w", padx=6)
            ctk.CTkLabel(panel.body, text=f"Correct: {ca}").pack(anchor="w", padx=6)
            ctk.CTkLabel(panel.body, text=f"Time: {rec['time_taken']:.1f}s").pack(anchor="w", padx=6)
