# ui/stats_view.py
import customtkinter as ctk
from ui.widgets.chart_panel import ChartPanel


class StatsView:
    def __init__(self, parent, state, stats_manager):
        self.frame = parent
        self.state = state
        self.stats = stats_manager
        self._build()

    def _build(self):
        summary = ctk.CTkFrame(self.frame)
        summary.pack(fill="x", pady=10)

        self.total_lbl = ctk.CTkLabel(summary, text="")
        self.total_lbl.pack(side="left", padx=10)

        self.avg_lbl = ctk.CTkLabel(summary, text="")
        self.avg_lbl.pack(side="left", padx=10)

        self.best_lbl = ctk.CTkLabel(summary, text="")
        self.best_lbl.pack(side="left", padx=10)

        self.chart = ChartPanel(self.frame)

        self.refresh()

    def refresh(self):
        s = self.state.stats
        self.total_lbl.configure(text=f"Total quizzes: {s['total_quizzes']}")
        self.avg_lbl.configure(text=f"Average: {s['average_score']:.1f}%")
        self.best_lbl.configure(text=f"Best: {s['best_score']:.1f}%")

        hist = self.stats.get_recent_history()
        self.chart.draw_score_history(hist)
