import logging
import sys

import customtkinter as ctk


class LogRedirector(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, out):
        try:
            self.text_widget.insert(ctk.END, out)
            self.text_widget.see(ctk.END)
        except:
            pass


class StdOutRedirect:
    def __init__(self, text_widget) -> None:
        self.text_widget = text_widget

    def write(self, out: str) -> None:
        try:
            self.text_widget.insert(ctk.END, out)
            self.text_widget.see(ctk.END)
        except:
            sys.out = out
            sys.stderr = out
