# main.py
import customtkinter as ctk

from core.app_config import AppConfig
from core.state import QuizState
from core.stats_manager import StatsManager

from services.quiz_engine import QuizEngine
from services.pdf_parser import PDFParser

from ui.quiz_view import QuizView
from ui.review_view import ReviewView
from ui.stats_view import StatsView
from ui.settings_view import SettingsView


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AWS Quiz App (Modern Refactor)")
        self.geometry("1280x840")

        # CTk defaults
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # -------------------------------------------------
        # Instantiate Core
        # -------------------------------------------------
        self.config_obj = AppConfig()                # loads quiz_config.json (if exists)
        self.quiz_state = QuizState(self.config_obj)
        self.engine = QuizEngine(self.quiz_state, self.config_obj)
        self.stats = StatsManager(self.quiz_state)
        self.pdf_parser = PDFParser()

        # -------------------------------------------------
        # Configure root layout
        # -------------------------------------------------
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        tab_quiz = self.tabview.add("Quiz")
        tab_review = self.tabview.add("Review")
        tab_stats = self.tabview.add("Statistics")
        tab_settings = self.tabview.add("Settings")

        # -------------------------------------------------
        # Instantiate UI views
        # -------------------------------------------------
        self.quiz_view = QuizView(
            tab_quiz,
            state=self.quiz_state,
            engine=self.engine,
            pdf_parser=self.pdf_parser,
            stats_manager=self.stats
        )

        self.review_view = ReviewView(
            tab_review,
            state=self.quiz_state
        )

        self.stats_view = StatsView(
            tab_stats,
            state=self.quiz_state,
            stats_manager=self.stats
        )

        self.settings_view = SettingsView(
            tab_settings,
            config=self.config_obj
        )


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
