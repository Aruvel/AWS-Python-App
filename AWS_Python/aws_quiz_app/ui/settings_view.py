# ui/settings_view.py
"""
Settings tab UI (binds to AppConfig instance).
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox


class SettingsView:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.frame = parent
        self._build_ui()

    def _build_ui(self):
        panel = ctk.CTkFrame(self.frame)
        panel.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(panel, text="Settings", font=("Arial", 16, "bold")).pack(anchor="w", padx=8, pady=(8, 16))

        # Randomize questions
        self.rand_var = tk.BooleanVar(value=getattr(self.config, "randomize_questions", True))
        ctk.CTkCheckBox(panel, text="Randomize question order", variable=self.rand_var).pack(anchor="w", padx=8, pady=6)

        # Show explanations
        self.exp_var = tk.BooleanVar(value=getattr(self.config, "show_explanations", True))
        ctk.CTkCheckBox(panel, text="Show explanations", variable=self.exp_var).pack(anchor="w", padx=8, pady=6)

        # Timer enabled
        self.timer_var = tk.BooleanVar(value=getattr(self.config, "timer_enabled", False))
        ctk.CTkCheckBox(panel, text="Enable timer", variable=self.timer_var).pack(anchor="w", padx=8, pady=6)

        # Time per question
        row = ctk.CTkFrame(panel)
        row.pack(fill="x", padx=8, pady=(12, 6))
        ctk.CTkLabel(row, text="Time per question (s)").pack(side="left")
        self.time_entry = ctk.CTkEntry(row, width=120)
        self.time_entry.insert(0, str(getattr(self.config, "time_per_question", 90)))
        self.time_entry.pack(side="right")

        # Exam time
        row2 = ctk.CTkFrame(panel)
        row2.pack(fill="x", padx=8, pady=(6, 12))
        ctk.CTkLabel(row2, text="Exam time limit (min)").pack(side="left")
        self.exam_entry = ctk.CTkEntry(row2, width=120)
        self.exam_entry.insert(0, str(getattr(self.config, "exam_time_limit", 90)))
        self.exam_entry.pack(side="right")

        # Save button
        btn = ctk.CTkButton(panel, text="💾 Save Settings", width=180, command=self.save)
        btn.pack(pady=12, padx=8)

    def save(self):
        # update config and save to disk (AppConfig.save)
        self.config.randomize_questions = self.rand_var.get()
        self.config.show_explanations = self.exp_var.get()
        self.config.timer_enabled = self.timer_var.get()
        try:
            self.config.time_per_question = int(self.time_entry.get())
        except ValueError:
            self.config.time_per_question = 90
        try:
            self.config.exam_time_limit = int(self.exam_entry.get())
        except ValueError:
            self.config.exam_time_limit = 90

        try:
            self.config.save("quiz_config.json")
            messagebox.showinfo("Settings", "Settings saved.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save settings: {e}")
