"""
UI Helper Functions
"""

import tkinter as tk
from typing import Tuple, Optional


class UIHelpers:
    """UI helper utilities"""
    
    @staticmethod
    def center_window(window, width: int, height: int) -> None:
        """Center a window on screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def get_color_for_score(score: float, is_exam: bool = False) -> str:
        """Get color based on score"""
        threshold = 70 if is_exam else 80
        
        if score >= 90:
            return "green"
        elif score >= threshold:
            return "blue"
        elif score >= 60:
            return "orange"
        else:
            return "red"
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Format seconds to MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 1) -> str:
        """Format percentage"""
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def create_tooltip(widget, text: str) -> None:
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background="yellow",
                relief="solid",
                borderwidth=1,
                font=("Arial", 10)
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    @staticmethod
    def validate_number_input(value: str, min_val: Optional[int] = None, 
                             max_val: Optional[int] = None) -> bool:
        """Validate number input"""
        if value == "":
            return True
        
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except ValueError:
            return False
    
    @staticmethod
    def bind_mousewheel(widget, canvas) -> None:
        """Bind mousewheel to scrollable widget"""
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        widget.bind("<MouseWheel>", on_mousewheel)
    
    @staticmethod
    def get_contrast_color(bg_color: str) -> str:
        """Get contrasting text color for background"""
        # Simple implementation - can be enhanced
        dark_colors = ["red", "blue", "darkgreen", "purple"]
        if bg_color in dark_colors:
            return "white"
        return "black"