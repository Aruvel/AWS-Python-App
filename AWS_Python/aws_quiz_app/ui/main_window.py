# ui/main_window.py
"""
Main customtkinter window, loads tabs and controllers
"""

import customtkinter as ctk
from ui.quiz_view import QuizView
from ui.review_view import ReviewView
from ui.stats_view import StatsView
from ui.settings_view import SettingsView


class MainWindow:

    def __init__(self, state, config, pdf_parser, engine):
        self.state = state
        self.config = config
        self.pdf_parser = pdf_parser
        self.engine = engine

        ctk.set_appearance_mode(config.theme)
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("AWS Quiz Pro — Refactored")
        self.root.geometry("1200x850")

        self.tabs = ctk.CTkTabview(self.root)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)

        # Instantiate views
        self.quiz_tab = QuizView(self.tabs.add("Quiz"), state, engine, pdf_parser)
        self.review_tab = ReviewView(self.tabs.add("Review"), state)
        self.stats_tab = StatsView(self.tabs.add("Statistics"), state)
        self.settings_tab = SettingsView(self.tabs.add("Settings"), config)

    def run(self):
        self.root.mainloop()
