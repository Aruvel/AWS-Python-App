"""
Main Application Window
"""

import customtkinter as ctk
from tkinter import messagebox
from config.settings import ConfigManager
from config.constants import *
from core.quiz_manager import QuizManager
from core.pdf_parser import PDFParser
from core.statistics import StatisticsManager
from ui.quiz_tab import QuizTab
from ui.review_tab import ReviewTab
from ui.stats_tab import StatsTab
from ui.settings_tab import SettingsTab


class MainWindow:
    """Main application window"""
    
    def __init__(self, pdf_filename=None):
        # Initialize main window
        self.root = ctk.CTk()
        self.root.geometry(DEFAULT_GEOMETRY)
        self.root.title(APP_TITLE)
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        
        # Initialize managers
        self.config_manager = ConfigManager(CONFIG_FILE)
        self.stats_manager = StatisticsManager(STATS_FILE)
        self.quiz_manager = QuizManager()
        self.pdf_parser = PDFParser(CACHE_PREFIX)
        
        # PDF filename
        self.pdf_filename = pdf_filename
        
        # Create UI
        self.create_ui()
        
        # Auto-load PDF if provided
        if pdf_filename:
            self.load_pdf(pdf_filename)
    
    def create_ui(self):
        """Create the main user interface"""
        # Create tabview
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create tabs
        self.quiz_tab = QuizTab(
            self.notebook.add("📝 Quiz"),
            self.quiz_manager,
            self.config_manager,
            self.on_load_pdf_clicked,
            self.on_quiz_finished
        )
        
        self.review_tab = ReviewTab(
            self.notebook.add("📋 Review"),
            self.quiz_manager
        )
        
        self.stats_tab = StatsTab(
            self.notebook.add("📊 Statistics"),
            self.stats_manager
        )
        
        self.settings_tab = SettingsTab(
            self.notebook.add("⚙️ Settings"),
            self.config_manager,
            self.on_settings_saved,
            self.on_clear_data
        )
    
    def on_load_pdf_clicked(self, filename=None):
        """Handle PDF load request"""
        if filename:
            self.pdf_filename = filename
        
        if self.pdf_filename:
            self.load_pdf(self.pdf_filename)
    
    def load_pdf(self, filename):
        """Load PDF file"""
        import threading
        
        def load():
            questions = self.pdf_parser.parse_pdf(filename)
            self.root.after(0, lambda: self.on_pdf_loaded(questions))
        
        self.quiz_tab.show_loading()
        threading.Thread(target=load, daemon=True).start()
    
    def on_pdf_loaded(self, questions):
        """Handle PDF loading completion"""
        if questions:
            self.quiz_manager.load_questions(questions)
            self.quiz_tab.on_questions_loaded(len(questions))
        else:
            messagebox.showerror("Error", "Failed to load questions from PDF")
            self.quiz_tab.on_questions_load_failed()
    
    def on_quiz_finished(self, results):
        """Handle quiz completion"""
        question_order = self.quiz_tab.get_question_order()
        self.stats_manager.record_quiz(results, question_order)
        self.stats_tab.update_display()
        
        # Update review tab
        self.review_tab.update_display()
    
    def on_settings_saved(self):
        """Handle settings save"""
        # Apply appearance mode
        appearance = self.config_manager.get("appearance_mode", "dark")
        ctk.set_appearance_mode(appearance)
        messagebox.showinfo("Settings", "Settings saved successfully!")
    
    def on_clear_data(self):
        """Handle data clear request"""
        confirm = messagebox.askyesno(
            "Clear Data",
            "This will reset all statistics and settings.\nAre you sure?"
        )
        
        if confirm:
            self.config_manager.reset()
            self.stats_manager.reset()
            self.stats_tab.update_display()
            messagebox.showinfo("Success", "All data has been reset.")
    
    def run(self):
        """Start the application"""
        self.stats_tab.update_display()
        self.root.mainloop()