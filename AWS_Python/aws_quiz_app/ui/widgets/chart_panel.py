
# ui/widgets/chart_panel.py
# Path: ui/widgets/chart_panel.py
"""
Small helper widget that renders a matplotlib Figure into a CTk frame.
Used by StatsView to display simple charts.
"""
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from datetime import datetime
from typing import List, Dict, Any


class ChartPanel:
    def __init__(self, parent: ctk.CTkFrame):
        self.parent = parent
        self.container = ctk.CTkFrame(parent)
        self.container.pack(fill="both", expand=True)
        self._canvas_widget = None

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()
        self._canvas_widget = None

    def draw_score_history(self, history: List[Dict[str, Any]]):
        """Draw a simple scores vs date line chart. history: list of records with 'date' and 'percentage'."""
        self.clear()
        if not history:
            ctk.CTkLabel(self.container, text="No history to show").pack(expand=True)
            return

        dates = []
        perc = []
        for rec in history:
            try:
                dates.append(datetime.fromisoformat(rec["date"]))
            except Exception:
                # fallback: treat as string
                dates.append(rec["date"])
            perc.append(rec.get("percentage", 0.0))

        fig = Figure(figsize=(7, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, perc, marker="o", linewidth=2)
        ax.set_title("Recent Scores")
        ax.set_ylabel("Percentage")
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=self.container)
        canvas.draw()
        self._canvas_widget = canvas.get_tk_widget()
        self._canvas_widget.pack(fill="both", expand=True, padx=8, pady=8)

