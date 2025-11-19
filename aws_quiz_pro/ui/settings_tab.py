"""
Settings Tab Interface
"""

import tkinter as tk
import customtkinter as ctk
from typing import Callable


class SettingsTab:
    """Settings interface tab"""
    
    def __init__(self, parent, config_manager, on_settings_saved: Callable, 
                 on_clear_data: Callable):
        self.parent = parent
        self.config_manager = config_manager
        self.on_settings_saved = on_settings_saved
        self.on_clear_data = on_clear_data
        
        self.create_ui()
    
    def create_ui(self):
        """Create settings interface"""
        settings_scroll = ctk.CTkScrollableFrame(self.parent)
        settings_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Quiz Settings
        self.create_quiz_settings(settings_scroll)
        
        # Exam Settings
        self.create_exam_settings(settings_scroll)
        
        # Data Management
        self.create_data_management(settings_scroll)
        
        # Save button
        ctk.CTkButton(
            settings_scroll,
            text="💾 Save Settings",
            command=self.save_settings,
            width=200,
            height=40
        ).pack(pady=20)
    
    def create_quiz_settings(self, parent):
        """Create quiz settings section"""
        quiz_settings_frame = ctk.CTkFrame(parent)
        quiz_settings_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            quiz_settings_frame,
            text="Quiz Settings",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 20))
        
        # Appearance mode
        self.appearance_mode = tk.StringVar(
            value=self.config_manager.get("appearance_mode", "dark")
        )
        ctk.CTkLabel(
            quiz_settings_frame,
            text="Appearance Mode:"
        ).pack(anchor="w", padx=20, pady=5)
        
        appearance_frame = ctk.CTkFrame(quiz_settings_frame)
        appearance_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkRadioButton(
            appearance_frame,
            text="Dark",
            variable=self.appearance_mode,
            value="dark"
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            appearance_frame,
            text="Light",
            variable=self.appearance_mode,
            value="light"
        ).pack(side="left", padx=5)
        
        # Default question order
        ctk.CTkLabel(
            quiz_settings_frame,
            text="Default Question Order:"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        order_setting_frame = ctk.CTkFrame(quiz_settings_frame)
        order_setting_frame.pack(fill="x", padx=20, pady=5)
        
        self.default_order_var = tk.StringVar(
            value=self.config_manager.get("default_question_order", "Random")
        )
        self.default_order_combo = ctk.CTkComboBox(
            order_setting_frame,
            values=["Random", "Sequential (First to Last)", "Reverse (Last to First)"],
            variable=self.default_order_var,
            width=250
        )
        self.default_order_combo.pack(side="left", padx=10)
        
        # Show explanations
        self.explanations_var = tk.BooleanVar(
            value=self.config_manager.get("show_explanations", True)
        )
        ctk.CTkCheckBox(
            quiz_settings_frame,
            text="Show explanations for wrong answers",
            variable=self.explanations_var
        ).pack(anchor="w", padx=20, pady=5)
        
        # Timer settings
        timer_frame = ctk.CTkFrame(quiz_settings_frame)
        timer_frame.pack(fill="x", padx=20, pady=10)
        
        self.timer_var = tk.BooleanVar(
            value=self.config_manager.get("timer_enabled", False)
        )
        ctk.CTkCheckBox(
            timer_frame,
            text="Enable timer",
            variable=self.timer_var
        ).pack(anchor="w", pady=5)
        
        timer_setting_frame = ctk.CTkFrame(timer_frame)
        timer_setting_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            timer_setting_frame,
            text="Time per question (seconds):"
        ).pack(side="left")
        
        self.timer_entry = ctk.CTkEntry(timer_setting_frame, width=100)
        self.timer_entry.insert(0, str(self.config_manager.get("time_per_question", 90)))
        self.timer_entry.pack(side="right", padx=10)
    
    def create_exam_settings(self, parent):
        """Create exam settings section"""
        exam_settings_frame = ctk.CTkFrame(parent)
        exam_settings_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            exam_settings_frame,
            text="Exam Settings",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 20))
        
        exam_timer_frame = ctk.CTkFrame(exam_settings_frame)
        exam_timer_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            exam_timer_frame,
            text="Exam time limit (minutes):"
        ).pack(side="left")
        
        self.exam_timer_entry = ctk.CTkEntry(exam_timer_frame, width=100)
        self.exam_timer_entry.insert(0, str(self.config_manager.get("exam_time_limit", 90)))
        self.exam_timer_entry.pack(side="right", padx=10)
    
    def create_data_management(self, parent):
        """Create data management section"""
        data_frame = ctk.CTkFrame(parent)
        data_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(
            data_frame,
            text="Data Management",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 10))
        
        ctk.CTkButton(
            data_frame,
            text="🧹 Clear All Data",
            command=self.on_clear_data,
            width=200,
            height=40
        ).pack(pady=10)
    
    def save_settings(self):
        """Save all settings"""
        self.config_manager.set("show_explanations", self.explanations_var.get())
        self.config_manager.set("timer_enabled", self.timer_var.get())
        self.config_manager.set("appearance_mode", self.appearance_mode.get())
        self.config_manager.set("default_question_order", self.default_order_var.get())
        
        try:
            self.config_manager.set("time_per_question", int(self.timer_entry.get()))
        except ValueError:
            self.config_manager.set("time_per_question", 90)
        
        try:
            self.config_manager.set("exam_time_limit", int(self.exam_timer_entry.get()))
        except ValueError:
            self.config_manager.set("exam_time_limit", 90)
        
        self.config_manager.save()
        self.on_settings_saved()