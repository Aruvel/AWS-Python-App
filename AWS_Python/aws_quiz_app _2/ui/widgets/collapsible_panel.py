# ui/widgets/collapsible_panel.py
# Path: ui/widgets/collapsible_panel.py
"""
A simple collapsible panel using customtkinter frames.
Header (clickable) toggles the body.
"""
import customtkinter as ctk
import tkinter as tk
from typing import Callable, Optional


class CollapsiblePanel(ctk.CTkFrame):
    def __init__(self, master, title: str = "", open_by_default: bool = False, header_command: Optional[Callable] = None, **kwargs):
        super().__init__(master, **kwargs)
        self._open = tk.BooleanVar(value=open_by_default)
        self._header_command = header_command
        self._build_ui(title)

    def _build_ui(self, title: str):
        self.header = ctk.CTkFrame(self)
        self.header.pack(fill="x")
        self.title_label = ctk.CTkLabel(self.header, text=title, cursor="hand2")
        self.title_label.pack(side="left", padx=8, pady=6)
        self.toggle_btn = ctk.CTkButton(self.header, text="▼" if self._open.get() else "▶", width=36, command=self.toggle)
        self.toggle_btn.pack(side="right", padx=6, pady=6)
        self.body = ctk.CTkFrame(self)
        if self._open.get():
            self.body.pack(fill="x", padx=6, pady=(0, 8))

        # bind header click
        self.title_label.bind("<Button-1>", lambda e: self.toggle())

    def toggle(self):
        if self._open.get():
            self.body.pack_forget()
            self._open.set(False)
            self.toggle_btn.configure(text="▶")
        else:
            self.body.pack(fill="x", padx=6, pady=(0, 8))
            self._open.set(True)
            self.toggle_btn.configure(text="▼")
        if callable(self._header_command):
            try:
                self._header_command(self._open.get())
            except Exception:
                pass


