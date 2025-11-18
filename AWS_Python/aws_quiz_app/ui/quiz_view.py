# ui/quiz_view.py
"""
Quiz tab UI.
Depends on:
 - state: core.state.QuizState
 - engine: services.quiz_engine.QuizEngine
 - pdf_parser: services.pdf_parser.PDFParser
"""
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from typing import Set

ctk.set_default_color_theme("blue")


class QuizView:
    def __init__(self, parent, state, engine, pdf_parser):
        self.parent = parent
        self.state = state
        self.engine = engine
        self.pdf_parser = pdf_parser

        self.frame = parent  # parent is a CTkFrame created by MainWindow
        self._build_ui()

        # runtime vars
        self._selected_radio = tk.IntVar(value=-1)
        self._selected_checks = []
        self._question_start_time = None

    def _build_ui(self):
        top = ctk.CTkFrame(self.frame)
        top.pack(fill="x", padx=12, pady=(8, 12))

        # left: load PDF
        load_btn = ctk.CTkButton(top, text="📁 Load PDF", width=140, command=self.load_pdf_dialog)
        load_btn.pack(side="left", padx=6)

        # mode selector
        self.mode_var = tk.StringVar(value="Practice")
        mode_label = ctk.CTkLabel(top, text="Mode:")
        mode_label.pack(side="left", padx=(12, 4))
        self.mode_combo = ctk.CTkComboBox(top, values=["Practice", "Exam"], variable=self.mode_var, width=150)
        self.mode_combo.pack(side="left", padx=(0, 12))

        # filters area (practice only)
        self.difficulty_var = tk.StringVar(value="All")
        diff_label = ctk.CTkLabel(top, text="Difficulty:")
        diff_label.pack(side="left", padx=(8, 4))
        self.diff_combo = ctk.CTkComboBox(top, values=["All", "Easy", "Medium", "Hard"],
                                           variable=self.difficulty_var, width=120)
        self.diff_combo.pack(side="left", padx=(0, 12))

        # start button
        self.start_btn = ctk.CTkButton(top, text="🚀 Start Quiz", width=140, command=self.start_quiz, state="disabled")
        self.start_btn.pack(side="right", padx=6)

        # progress frame
        progress = ctk.CTkFrame(self.frame)
        progress.pack(fill="x", padx=12, pady=(0, 10))

        self.progress_label = ctk.CTkLabel(progress, text="No quiz loaded", anchor="w")
        self.progress_label.pack(side="left", padx=6, pady=8)

        self.score_label = ctk.CTkLabel(progress, text="Score: 0/0")
        self.score_label.pack(side="right", padx=6, pady=8)

        self.progress_bar = ctk.CTkProgressBar(progress)
        self.progress_bar.pack(fill="x", padx=6, pady=(0, 8))

        # question area
        self.q_frame = ctk.CTkScrollableFrame(self.frame, height=360)
        self.q_frame.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        self.q_text = ctk.CTkLabel(self.q_frame, text="Load a PDF to begin.", wraplength=900, justify="left",
                                   font=("Arial", 14))
        self.q_text.pack(anchor="w", padx=12, pady=12)

        self.options_container = ctk.CTkFrame(self.q_frame)
        self.options_container.pack(fill="x", padx=12, pady=6)

        # feedback & buttons
        bottom = ctk.CTkFrame(self.frame)
        bottom.pack(fill="x", padx=12, pady=8)

        self.feedback_label = ctk.CTkLabel(bottom, text="", anchor="w")
        self.feedback_label.pack(fill="x", padx=6, pady=(0, 8))

        btns = ctk.CTkFrame(bottom)
        btns.pack(fill="x", padx=6, pady=6)

        self.submit_btn = ctk.CTkButton(btns, text="✓ Submit Answer", width=150, state="disabled",
                                        command=self.submit_answer)
        self.submit_btn.pack(side="left", padx=6)

        self.next_btn = ctk.CTkButton(btns, text="Next →", width=120, state="disabled", command=self.next_question)
        self.next_btn.pack(side="left", padx=6)

        self.hint_btn = ctk.CTkButton(btns, text="💡 Hint", width=100, command=self.show_hint, state="disabled")
        self.hint_btn.pack(side="left", padx=6)

    # -------------------------
    # PDF load (background)
    # -------------------------
    def load_pdf_dialog(self):
        filename = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF", "*.pdf"), ("All", "*.*")])
        if not filename:
            return
        # disable start until parsed
        self.progress_label.configure(text="📚 Parsing PDF...")
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self._load_pdf_bg, args=(filename,), daemon=True).start()

    def _load_pdf_bg(self, filename):
        try:
            questions = self.pdf_parser.load(filename)
        except Exception as e:
            self.frame.after(0, lambda: messagebox.showerror("PDF Error", f"Failed to parse PDF: {e}"))
            self.frame.after(0, lambda: self.progress_label.configure(text="Failed to parse PDF"))
            return
        # hand to engine
        self.engine.load_questions(questions)
        self.frame.after(0, lambda: self.on_pdf_loaded(len(questions)))

    def on_pdf_loaded(self, count: int):
        self.progress_label.configure(text=f"✅ Loaded {count} questions")
        self.start_btn.configure(state="normal")
        # populate difficulty options from loaded questions
        difficulties = {"All"}
        for q in self.engine.state.questions:
            diff = getattr(q, "difficulty", "Medium")
            difficulties.add(diff)
        self.diff_combo.configure(values=sorted(list(difficulties)))

    # -------------------------
    # Quiz lifecycle
    # -------------------------
    def start_quiz(self):
        if not self.engine.state.questions:
            messagebox.showwarning("No questions", "Please load a PDF first.")
            return

        mode = self.mode_var.get()
        if mode == "Exam":
            # require at least 65 or let engine handle sample size check
            try:
                self.engine.start_exam_mode(count=65)
            except Exception:
                # fallback: allow full set
                self.engine.start_exam_mode(count=min(65, len(self.engine.state.questions)))
        else:
            self.engine.state.exam_mode = False
            # apply filters
            self.engine.apply_filters(difficulty=self.difficulty_var.get())

        # reset UI/state
        self.engine.state.current_index = 0
        self.engine.state.score = 0
        self.feedback_label.configure(text="")
        self.submit_btn.configure(state="normal")
        self.next_btn.configure(state="disabled")
        if not self.engine.state.exam_mode:
            self.hint_btn.configure(state="normal")
        else:
            self.hint_btn.configure(state="disabled")

        self.load_question()

    def load_question(self):
        idx = self.engine.state.current_index
        if idx >= len(self.engine.state.filtered):
            self.finish_quiz()
            return

        q = self.engine.state.filtered[idx]
        total = len(self.engine.state.filtered)
        self.progress_label.configure(text=f"{'EXAM' if self.engine.state.exam_mode else 'Practice'} | Q {idx+1}/{total} | Topic: {q.topic}")
        self.progress_bar.set((idx) / total)
        # question text
        self.q_text.configure(text=f"Q{idx+1}: {q.question}")

        # clear options
        for w in self.options_container.winfo_children():
            w.destroy()

        # reset selection variables
        if len(q.correct_answers) == 1:
            self._selected_radio.set(-1)
            for i, opt in enumerate(q.options):
                r = ctk.CTkRadioButton(self.options_container, text=f"{chr(65+i)}. {opt}",
                                       variable=self._selected_radio, value=i)
                r.pack(anchor="w", padx=8, pady=4)
            self._selected_checks = []
        else:
            self._selected_checks = []
            for i, opt in enumerate(q.options):
                var = tk.IntVar(value=0)
                cb = ctk.CTkCheckBox(self.options_container, text=f"{chr(65+i)}. {opt}", variable=var)
                cb.pack(anchor="w", padx=8, pady=4)
                self._selected_checks.append(var)

        # reset buttons and timers
        self.submit_btn.configure(state="normal")
        self.next_btn.configure(state="disabled")
        self.feedback_label.configure(text="")
        self._question_start_time = datetime.now()

        # update score label
        self.score_label.configure(text=f"Score: {self.engine.state.score}/{idx}")

    def _gather_user_answer(self) -> Set[int]:
        q = self.engine.state.filtered[self.engine.state.current_index]
        if len(q.correct_answers) == 1:
            val = self._selected_radio.get()
            return {val} if val >= 0 else set()
        else:
            return {i for i, var in enumerate(self._selected_checks) if var.get()}

    def submit_answer(self):
        if self.submit_btn.cget("state") == "disabled":
            return
        user_set = self._gather_user_answer()
        if not user_set:
            messagebox.showwarning("No answer", "Please select at least one option.")
            return

        is_correct = self.engine.submit_answer(user_set)
        elapsed = (datetime.now() - self._question_start_time).total_seconds() if self._question_start_time else 0.0
        # store minimal answered record to state for review (simple format)
        answered_record = {
            "question": self.engine.state.filtered[self.engine.state.current_index],
            "user_answer": user_set,
            "is_correct": is_correct,
            "time_taken": elapsed,
            "question_number": self.engine.state.current_index + 1
        }
        # attach to engine/state for review convenience
        if not hasattr(self.engine.state, "answered_questions"):
            self.engine.state.answered_questions = []
        self.engine.state.answered_questions.append(answered_record)

        if is_correct:
            self.feedback_label.configure(text="🎉 Correct!", text_color="green")
        else:
            correct_letters = ", ".join(chr(65 + i) for i in sorted(self.engine.state.filtered[self.engine.state.current_index].correct_answers))
            self.feedback_label.configure(text=f"❌ Incorrect — Correct: {correct_letters}", text_color="red")

        # update score label
        idx = self.engine.state.current_index
        self.score_label.configure(text=f"Score: {self.engine.state.score}/{idx+1}")

        self.submit_btn.configure(state="disabled")
        self.next_btn.configure(state="normal")
        # if last question, rename Next -> Finish
        if self.engine.state.current_index >= len(self.engine.state.filtered) - 1:
            self.next_btn.configure(text="Finish")
        else:
            self.next_btn.configure(text="Next →")

    def next_question(self):
        # advance; engine.next_question returns False if no more questions
        has_more = self.engine.next_question()
        if has_more:
            self.load_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        total = len(self.engine.state.filtered)
        score = self.engine.state.score
        pct = (score / total * 100) if total else 0.0
        message = f"Finished! Score: {score}/{total} ({pct:.1f}%)"
        messagebox.showinfo("Quiz Complete", message)
        # allow re-start
        self.start_btn.configure(state="normal")
        self.submit_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        self.progress_bar.set(1.0)

    def show_hint(self):
        # simple hint: remove one wrong option for single-choice only
        idx = self.engine.state.current_index
        q = self.engine.state.filtered[idx]
        if len(q.correct_answers) != 1 or self.engine.state.exam_mode:
            return
        wrong = [i for i in range(len(q.options)) if i not in q.correct_answers]
        if not wrong:
            return
        import random
        eliminated = random.choice(wrong)
        messagebox.showinfo("Hint", f"You can eliminate option {chr(65+eliminated)}")