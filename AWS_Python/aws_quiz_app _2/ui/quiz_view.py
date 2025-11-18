# ui/quiz_view.py
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from datetime import datetime
from ui.widgets.question_widget import QuestionWidget
from services.timer import CountdownTimer


class QuizView:
    def __init__(self, parent, state, engine, pdf_parser, stats_manager):
        self.parent = parent
        self.state = state
        self.engine = engine
        self.pdf_parser = pdf_parser
        self.stats = stats_manager

        self.frame = parent
        self._question_widget = None
        self._timer = None
        self._question_start_time = None

        self._build_ui()

    def _build_ui(self):
        top = ctk.CTkFrame(self.frame)
        top.pack(fill="x", pady=10)

        btn_load = ctk.CTkButton(top, text="📁 Load PDF", command=self.load_pdf_dialog)
        btn_load.pack(side="left", padx=10)

        self.mode_var = tk.StringVar(value="Practice")
        self.mode_box = ctk.CTkComboBox(top, values=["Practice", "Exam"], variable=self.mode_var)
        self.mode_box.pack(side="left", padx=10)

        self.diff_var = tk.StringVar(value="All")
        self.diff_box = ctk.CTkComboBox(top, values=["All", "Easy", "Medium", "Hard"], variable=self.diff_var)
        self.diff_box.pack(side="left", padx=10)

        self.start_btn = ctk.CTkButton(top, text="Start Quiz", state="disabled", command=self.start_quiz)
        self.start_btn.pack(side="right", padx=10)

        # Progress
        progress_frame = ctk.CTkFrame(self.frame)
        progress_frame.pack(fill="x", pady=8)

        self.progress_label = ctk.CTkLabel(progress_frame, text="Load PDF to begin")
        self.progress_label.pack(side="left", padx=10)

        self.timer_label = ctk.CTkLabel(progress_frame, text="")
        self.timer_label.pack(side="right", padx=10)

        # Question area
        self.q_area = ctk.CTkScrollableFrame(self.frame, height=450)
        self.q_area.pack(fill="both", expand=True, pady=10)

        # Bottom controls
        bottom = ctk.CTkFrame(self.frame)
        bottom.pack(fill="x", pady=10)

        self.feedback_label = ctk.CTkLabel(bottom, text="")
        self.feedback_label.pack(fill="x", padx=10)

        btns = ctk.CTkFrame(bottom)
        btns.pack()

        self.submit_btn = ctk.CTkButton(btns, text="Submit", state="disabled", command=self.submit_answer)
        self.submit_btn.pack(side="left", padx=10)

        self.next_btn = ctk.CTkButton(btns, text="Next", state="disabled", command=self.next_question)
        self.next_btn.pack(side="left", padx=10)

    # -------------------------
    # PDF load
    # -------------------------
    def load_pdf_dialog(self):
        file = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if not file:
            return
        self.progress_label.configure(text="Parsing PDF...")

        def worker():
            try:
                questions = self.pdf_parser.load(file)
                self.engine.load_questions(questions)
                self.frame.after(0, lambda: self.on_pdf_loaded(len(questions)))
            except Exception as e:
                messagebox.showerror("PDF Error", str(e))

        threading.Thread(target=worker, daemon=True).start()

    def on_pdf_loaded(self, count):
        self.progress_label.configure(text=f"Loaded {count} questions")
        self.start_btn.configure(state="normal")

    # -------------------------
    # Quiz lifecycle
    # -------------------------
    def start_quiz(self):
        mode = self.mode_var.get()

        if mode == "Exam":
            self.engine.start_exam_mode(count=65)
            self._start_exam_timer()
        else:
            self.engine.state.exam_mode = False
            self.engine.apply_filters(difficulty=self.diff_var.get())

        self.next_btn.configure(state="disabled")
        self.submit_btn.configure(state="normal")
        self.load_question()

    def _start_exam_timer(self):
        limit_min = getattr(self.engine.config, "exam_time_limit", 90)
        seconds = limit_min * 60

        def tick(rem):
            self.timer_label.configure(text=f"Time left: {rem//60:02d}:{rem%60:02d}")

        def finished():
            messagebox.showinfo("Time Up", "Exam time has expired!")
            self.finish_quiz()

        self._timer = CountdownTimer(seconds, tick_cb=tick, finish_cb=finished)
        self._timer.start()

    def load_question(self):
        self._clear_question()
        idx = self.engine.state.current_index
        if idx >= len(self.engine.state.filtered):
            self.finish_quiz()
            return

        q = self.engine.state.filtered[idx]
        total = len(self.engine.state.filtered)
        self.progress_label.configure(text=f"Q {idx+1}/{total} | Topic: {q.topic}")

        self._question_widget = QuestionWidget(
            master=self.q_area,
            question_text=q.question,
            options=q.options,
            multi=len(q.correct_answers) > 1,
        )
        self._question_widget.pack(fill="x", padx=10, pady=10)

        self.submit_btn.configure(state="normal")
        self.next_btn.configure(state="disabled")
        self.feedback_label.configure(text="")
        self._question_start_time = datetime.now()

    def _clear_question(self):
        for w in self.q_area.winfo_children():
            w.destroy()

    def submit_answer(self):
        ans = self._question_widget.get_user_answer()
        if not ans:
            messagebox.showwarning("No answer", "Select at least one option")
            return

        is_correct = self.engine.submit_answer(ans)
        elapsed = (datetime.now() - self._question_start_time).total_seconds()

        if is_correct:
            self.feedback_label.configure(text="Correct!", text_color="green")
        else:
            correct = self.engine.state.filtered[self.engine.state.current_index].correct_answers
            letters = ", ".join(chr(65+i) for i in correct)
            self.feedback_label.configure(text=f"Wrong. Correct: {letters}", text_color="red")

        # Save review record
        self.state.answered_questions.append({
            "question": self.engine.state.filtered[self.engine.state.current_index],
            "user_answer": ans,
            "is_correct": is_correct,
            "time_taken": elapsed,
            "question_number": self.engine.state.current_index + 1
        })

        self.submit_btn.configure(state="disabled")
        self.next_btn.configure(state="normal")

    def next_question(self):
        if self.engine.next_question():
            self.load_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        if self._timer:
            self._timer.cancel()

        total = len(self.engine.state.filtered)
        score = self.engine.state.score
        wrong = total - score
        elapsed = sum(item["time_taken"] for item in self.state.answered_questions if "time_taken" in item)

        self.stats.record_quiz(score, total, elapsed, wrong, self.state.exam_mode)

        pct = (score / total) * 100 if total else 0
        messagebox.showinfo("Finished", f"Score: {score}/{total} ({pct:.1f}%)")

        self.submit_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        self.start_btn.configure(state="normal")
