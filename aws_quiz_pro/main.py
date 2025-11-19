"""
AWS Quiz Pro - Main Entry Point
"""

import sys
import os
import customtkinter as ctk
from ui.main_window import MainWindow


def main():
    """Main entry point"""
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Check if PDF filename provided as argument
    pdf_file = None
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
    
    # Create and run the app
    app = MainWindow(pdf_file)
    app.run()


if __name__ == "__main__":
    main()