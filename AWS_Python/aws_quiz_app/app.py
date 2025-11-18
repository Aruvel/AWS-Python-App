# app.py
"""
AWS Quiz App — Refactored Entry Point
Clean, modular, maintainable replacement for the monolithic script.
"""

from ui.main_window import MainWindow
from core.config import AppConfig
from core.state import QuizState
from services.pdf_parser import PDFParser
from services.quiz_engine import QuizEngine


def main():
    # Load configuration & state
    config = AppConfig.load("quiz_config.json")
    state = QuizState(config=config)

    # Create services
    pdf_parser = PDFParser(cache_dir="cache")
    engine = QuizEngine(state=state, config=config)

    # Start the UI
    app = MainWindow(
        state=state,
        config=config,
        pdf_parser=pdf_parser,
        engine=engine
    )

    app.run()


if __name__ == "__main__":
    main()
