
# ui/stats_view.py
"""
Statistics tab UI. Requires state.stats or an external stats_manager to populate.
"""
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from datetime import datetime


class StatsView:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.frame = parent
        self._build_ui()
        # call update when stats change
        self.update_summary()

    def _build_ui(self):
        header = ctk.CTkFrame(self.frame)
        header.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(header, text="📊 Statistics", font=("Arial", 16, "bold")).pack(side="left", padx=8)

        self.summary_frame = ctk.CTkFrame(self.frame)
        self.summary_frame.pack(fill="x", padx=12, pady=(4, 12))

        self.total_label = ctk.CTkLabel(self.summary_frame, text="Total Quizzes: 0")
        self.total_label.pack(side="left", padx=8)
        self.avg_label = ctk.CTkLabel(self.summary_frame, text="Average: 0%")
        self.avg_label.pack(side="left", padx=8)
        self.best_label = ctk.CTkLabel(self.summary_frame, text="Best: 0%")
        self.best_label.pack(side="left", padx=8)

        # charts area
        self.chart_frame = ctk.CTkFrame(self.frame)
        self.chart_frame.pack(fill="both", expand=True, padx=12, pady=8)

    def update_summary(self):
        stats = getattr(self.state, "stats", None)
        if not stats:
            self.total_label.configure(text="Total Quizzes: 0")
            self.avg_label.configure(text="Average: 0%")
            self.best_label.configure(text="Best: 0%")
            return

        self.total_label.configure(text=f"Total Quizzes: {stats.get('total_quizzes', 0)}")
        self.avg_label.configure(text=f"Average: {stats.get('average_score', 0):.1f}%")
        self.best_label.configure(text=f"Best: {stats.get('best_score', 0):.1f}%")
        self.draw_score_history()

    def draw_score_history(self):
        # clear chart frame
        for w in self.chart_frame.winfo_children():
            w.destroy()

        stats = getattr(self.state, "stats", {})
        history = (stats.get("quiz_history", []) + stats.get("exam_history", []))[-20:]
        if not history:
            ctk.CTkLabel(self.chart_frame, text="No history yet", font=("Arial", 12)).pack(expand=True)
            return

        # build simple line chart of percentages
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        dates = [datetime.fromisoformat(h["date"]) for h in history]
        perc = [h["percentage"] for h in history]
        ax.plot(dates, perc, marker="o", linewidth=2)
        ax.set_title("Recent Scores")
        ax.set_ylabel("Percentage")
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)


