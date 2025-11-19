"""
Statistics Tab Interface
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import numpy as np


class StatsTab:
    """Statistics interface tab"""
    
    def __init__(self, parent, stats_manager):
        self.parent = parent
        self.stats_manager = stats_manager
        
        self.create_ui()
    
    def create_ui(self):
        """Create statistics interface"""
        # Summary cards
        summary_frame = ctk.CTkFrame(self.parent)
        summary_frame.pack(fill="x", padx=10, pady=10)
        
        stats_container = ctk.CTkFrame(summary_frame)
        stats_container.pack(fill="x", padx=10, pady=10)
        
        # Total quizzes card
        quiz_card = ctk.CTkFrame(stats_container)
        quiz_card.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(quiz_card, text="Total Quizzes", font=("Arial", 12)).pack(pady=(10, 5))
        self.total_quizzes_label = ctk.CTkLabel(quiz_card, text="0", font=("Arial", 24, "bold"))
        self.total_quizzes_label.pack(pady=(0, 10))
        
        # Average score card
        avg_card = ctk.CTkFrame(stats_container)
        avg_card.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(avg_card, text="Average Score", font=("Arial", 12)).pack(pady=(10, 5))
        self.avg_score_label = ctk.CTkLabel(avg_card, text="0%", font=("Arial", 24, "bold"))
        self.avg_score_label.pack(pady=(0, 10))
        
        # Best score card
        best_card = ctk.CTkFrame(stats_container)
        best_card.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(best_card, text="Best Score", font=("Arial", 12)).pack(pady=(10, 5))
        self.best_score_label = ctk.CTkLabel(best_card, text="0%", font=("Arial", 24, "bold"))
        self.best_score_label.pack(pady=(0, 10))
        
        # Exam attempts card
        exam_card = ctk.CTkFrame(stats_container)
        exam_card.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(exam_card, text="Exam Attempts", font=("Arial", 12)).pack(pady=(10, 5))
        self.exam_attempts_label = ctk.CTkLabel(exam_card, text="0", font=("Arial", 24, "bold"))
        self.exam_attempts_label.pack(pady=(0, 10))
        
        # Charts frame
        self.charts_frame = ctk.CTkFrame(self.parent)
        self.charts_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def update_display(self):
        """Update statistics display"""
        summary = self.stats_manager.get_summary()
        
        self.total_quizzes_label.configure(text=str(summary["total_quizzes"]))
        self.avg_score_label.configure(text=f"{summary['average_score']:.1f}%")
        self.best_score_label.configure(text=f"{summary['best_score']:.1f}%")
        self.exam_attempts_label.configure(text=str(summary["exam_attempts"]))
        
        self.update_charts()
    
    def update_charts(self):
        """Update statistics charts"""
        try:
            # Clear existing charts
            for widget in self.charts_frame.winfo_children():
                widget.destroy()
            
            quiz_history = self.stats_manager.stats.get("quiz_history", [])
            exam_history = self.stats_manager.stats.get("exam_history", [])
            
            if not quiz_history and not exam_history:
                ctk.CTkLabel(
                    self.charts_frame,
                    text="No quiz history available yet",
                    font=("Arial", 14)
                ).pack(expand=True)
                return
            
            # Create matplotlib figure
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            fig.patch.set_facecolor('#2b2b2b')
            plt.style.use('dark_background')
            
            # Chart 1: Score history
            self.create_score_history_chart(ax1, quiz_history, exam_history)
            
            # Chart 2: Score distribution
            self.create_score_distribution_chart(ax2, quiz_history, exam_history)
            
            # Chart 3: Pass/Fail rate
            self.create_pass_rate_chart(ax3, exam_history)
            
            # Chart 4: Performance trend
            self.create_trend_chart(ax4, quiz_history, exam_history)
            
            plt.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.charts_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.charts_frame,
                text=f"Error loading charts: {str(e)}",
                font=("Arial", 12)
            )
            error_label.pack(expand=True)
            import traceback
            print(f"Chart error: {traceback.format_exc()}")
    
    def create_score_history_chart(self, ax, quiz_history, exam_history):
        """Create score history chart"""
        all_history = sorted(quiz_history + exam_history, key=lambda x: x["date"])[-20:]
        
        if all_history:
            dates = [datetime.fromisoformat(h["date"]).strftime("%m/%d") for h in all_history]
            scores = [h["percentage"] for h in all_history]
            colors = ['red' if h.get("is_exam", False) else 'blue' for h in all_history]
            
            for i, (date, score, color) in enumerate(zip(dates, scores, colors)):
                ax.scatter(i, score, c=color, s=60, alpha=0.7)
            
            ax.plot(range(len(scores)), scores, alpha=0.3, color='gray')
            ax.set_title("Score History (Red=Exam, Blue=Practice)", fontsize=12, fontweight='bold')
            ax.set_ylabel("Score (%)")
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=45)
            ax.grid(True, alpha=0.3)
            ax.axhline(y=70, color='green', linestyle='--', alpha=0.5, label='Pass Line')
            ax.legend()
        else:
            ax.text(0.5, 0.5, "No data yet", ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title("Score History", fontsize=12, fontweight='bold')
    
    def create_score_distribution_chart(self, ax, quiz_history, exam_history):
        """Create score distribution chart"""
        if exam_history and quiz_history:
            exam_scores = [h["percentage"] for h in exam_history]
            quiz_scores = [h["percentage"] for h in quiz_history[-len(exam_history):]]
            
            ax.boxplot([quiz_scores, exam_scores], labels=['Practice', 'Exam'])
            ax.set_title("Practice vs Exam Performance", fontsize=12, fontweight='bold')
            ax.set_ylabel("Score (%)")
            ax.grid(True, alpha=0.3)
        elif exam_history:
            exam_scores = [h["percentage"] for h in exam_history]
            ax.hist(exam_scores, bins=5, alpha=0.7, color='red', edgecolor='black')
            ax.set_title("Exam Score Distribution", fontsize=12, fontweight='bold')
            ax.set_ylabel("Frequency")
            ax.set_xlabel("Score (%)")
        elif quiz_history:
            quiz_scores = [h["percentage"] for h in quiz_history]
            ax.hist(quiz_scores, bins=10, alpha=0.7, color='blue', edgecolor='black')
            ax.set_title("Practice Score Distribution", fontsize=12, fontweight='bold')
            ax.set_ylabel("Frequency")
            ax.set_xlabel("Score (%)")
        else:
            ax.text(0.5, 0.5, "Need more data", ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title("Score Distribution", fontsize=12, fontweight='bold')
    
    def create_pass_rate_chart(self, ax, exam_history):
        """Create pass/fail rate pie chart"""
        if exam_history:
            passed = sum(1 for h in exam_history if h.get("passed", False))
            failed = len(exam_history) - passed
            
            if passed > 0 or failed > 0:
                ax.pie([passed, failed], labels=['Passed', 'Failed'],
                      colors=['green', 'red'], autopct='%1.1f%%')
                ax.set_title("Exam Pass Rate", fontsize=12, fontweight='bold')
            else:
                ax.text(0.5, 0.5, "No exam data", ha='center', va='center',
                       transform=ax.transAxes, fontsize=12)
                ax.set_title("Exam Pass Rate", fontsize=12, fontweight='bold')
        else:
            ax.text(0.5, 0.5, "No exam attempts yet", ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title("Exam Pass Rate", fontsize=12, fontweight='bold')
    
    def create_trend_chart(self, ax, quiz_history, exam_history):
        """Create performance trend chart"""
        all_history = sorted(quiz_history + exam_history, key=lambda x: x["date"])
        
        if len(all_history) >= 3:
            recent_history = all_history[-10:]
            scores = [h["percentage"] for h in recent_history]
            x_vals = list(range(len(scores)))
            
            ax.plot(x_vals, scores, marker='o', linewidth=2, markersize=6)
            
            # Add trend line
            if len(scores) > 2:
                z = np.polyfit(x_vals, scores, 1)
                p = np.poly1d(z)
                ax.plot(x_vals, p(x_vals), "--", alpha=0.7, color='orange')
            
            ax.set_title("Recent Performance Trend", fontsize=12, fontweight='bold')
            ax.set_ylabel("Score (%)")
            ax.set_xlabel("Attempt")
            ax.grid(True, alpha=0.3)
            
            # Show trend direction
            if len(scores) >= 2:
                trend = "↑" if scores[-1] > scores[0] else "↓"
                ax.text(0.02, 0.98, trend, transform=ax.transAxes,
                       fontsize=20, va='top')
        else:
            ax.text(0.5, 0.5, "Need more data\n(3+ attempts)", ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title("Performance Trend", fontsize=12, fontweight='bold')