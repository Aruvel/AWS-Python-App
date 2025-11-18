# ui/widgets/question_widget.py
# Path: ui/widgets/question_widget.py
"""
Question rendering widget. Use to display a Question model and collect user input.
Exposes get_user_answer() -> set[int]
"""
import customtkinter as ctk
import tkinter as tk
from typing import List, Set, Optional


class QuestionWidget(ctk.CTkFrame):
    def __init__(self, master, question_text: str, options: List[str], multi: bool = False, **kwargs):
        super().__init__(master, **kwargs)
        self.question_text = question_text
        self.options = options
        self.multi = multi
        self._build()

    def _build(self):
        self.q_label = ctk.CTkLabel(self, text=self.question_text, wraplength=900, justify="left", font=("Arial", 13))
        self.q_label.pack(anchor="w", padx=8, pady=(6, 10))

        self.option_vars = []
        self.option_widgets = []

        if not self.multi:
            self._radio_var = tk.IntVar(value=-1)
            for i, opt in enumerate(self.options):
                r = ctk.CTkRadioButton(self, text=f"{chr(65+i)}. {opt}", variable=self._radio_var, value=i)
                r.pack(anchor="w", padx=12, pady=4)
                self.option_widgets.append(r)
        else:
            for i, opt in enumerate(self.options):
                v = tk.IntVar(value=0)
                cb = ctk.CTkCheckBox(self, text=f"{chr(65+i)}. {opt}", variable=v)
                cb.pack(anchor="w", padx=12, pady=4)
                self.option_vars.append(v)
                self.option_widgets.append(cb)

    def get_user_answer(self) -> Set[int]:
        if not self.multi:
            val = self._radio_var.get()
            return {val} if val >= 0 else set()
        else:
            return {i for i, v in enumerate(self.option_vars) if v.get()}


