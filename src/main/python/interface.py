import os
import re
import subprocess
from tkinter import Frame, IntVar

import customtkinter as tk


class InterfaceApp:
    """
    A generic tester application with a graphical user interface for running tests.

    Attributes:
        root (tk.CTk): The main application window.
        base_command (str): The base command for running tests.
        tests (list): A list of tests, each represented as a tuple of (command, label).
        title (str): The title of the application.
        console (tk.CTkScrollableFrame): The frame to display test output.
    """

    DEFAULT_GEOMETRY = "1250x580"
    DEFAULT_APPEARANCE = "dark"
    DEFAULT_COLOR_THEME = "blue"
    VALUES_APPEARANCE = ["Dark", "Light"]
    TERMINAL_FONT = "Consolas"

    def __init__(self, logs: list) -> None:
        self.root = tk.CTk()
        self.logs = logs


        self.console = tk.CTkScrollableFrame(self.root, width=300, height=800)
        self.console.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.initialize()

    def initialize(self):
        self.setup_appearance()
        self.create_gui()
        self.root.mainloop()

    def set_appearance_mode(self, new_appearance_mode: str):
        tk.set_appearance_mode(new_appearance_mode)

    def setup_appearance(self):
        tk.set_appearance_mode(self.DEFAULT_APPEARANCE)
        tk.set_default_color_theme(self.DEFAULT_COLOR_THEME)
    def create_gui(self):
        self.root.geometry(self.DEFAULT_GEOMETRY)
        self.root.title("Integrity Check HIDS")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)

        self.create_sidebar()

    def create_sidebar(self):
        sidebar_frame = tk.CTkFrame(self.root, width=140, corner_radius=0,border_color="Red")
        sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebar_frame.grid_rowconfigure(1, weight=1)


        self.tabview = tk.CTkTabview(sidebar_frame, width=300, height=800)
        self.tabview.grid(padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Historial de Logs")
        self.tabview.add("Verificación de Integridad")


        self.create_log_buttons()
        self.create_appearance_options(sidebar_frame)


    def create_appearance_options(self, parent_frame: Frame) -> None:
        appearance_mode_label = tk.CTkLabel(parent_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionmenu = tk.CTkOptionMenu(parent_frame, values=self.VALUES_APPEARANCE,
                                                      command=self.change_appearance_mode_event)
        appearance_mode_optionmenu.grid(row=1, column=0, padx=20, pady=(10, 10))

    def create_log_buttons(self):
        frame = self.tabview.tab("Historial de Logs")

        logs = []
        logs_frame = tk.CTkScrollableFrame(frame)
        logs_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        for index, (name) in enumerate(self.logs):
            log_button = tk.CTkButton(logs_frame, text=name,fg_color="transparent",
                                    command=lambda file=name: self.display_output(file))
            log_button.grid(row=index + 1, column=0, padx=10, sticky="w")
            logs.append(log_button)


    def display_output(self, file:str):
        for widget in self.console.winfo_children():
            widget.destroy()
        ruta_elemento = os.path.join("../logs", file)
        with open(ruta_elemento, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            title_label=tk.CTkLabel(self.console, text=file,
                                          font=tk.CTkFont(family=self.TERMINAL_FONT, size=20, weight="bold"))
            title_label.pack(side="top", anchor="w")
            contenido_label = tk.CTkLabel(self.console, text=contenido,
                                          font=tk.CTkFont(family=self.TERMINAL_FONT, size=15))
            contenido_label.pack(side="top", anchor="w")


    def change_appearance_mode_event(self, mode: str) -> None:
        """
        Event handler for changing the appearance mode.

        :param mode: The selected appearance mode.
        """
        tk.set_appearance_mode(mode)
class InterfaceHIDS(InterfaceApp):
    def __init__(self):
        logs= os.listdir("../logs")
        super().__init__(logs=logs)


if __name__ == '__main__':
    app = InterfaceHIDS()

