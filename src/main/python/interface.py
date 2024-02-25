import os
from tkinter import Frame

import customtkinter as ctk

from src.main.python.client import Client
from src.main.python.logger import Logger

class InterfaceHIDS:
    DEFAULT_GEOMETRY = "1250x580"
    DEFAULT_APPEARANCE = "dark"
    DEFAULT_COLOR_THEME = "blue"
    VALUES_APPEARANCE = ["Dark", "Light"]
    TERMINAL_FONT = "Consolas"

    def __init__(self, host, port, logs_path="../logs", files_path="../resources") -> None:
        """
        Initializes the InterfaceHIDS class.

        Args:
            logs_path (str): Path to the logs directory.
            files_path (str): Path to the resources directory.
        """
        self.root = ctk.CTk()
        self.logs = os.listdir(logs_path)
        self.files = [file for _, _, aux_files in os.walk(files_path) for file in aux_files if "." in file]
        self.client = Client(host, port)
        self.client.connect()


        self.console = ctk.CTkScrollableFrame(self.root, width=300, height=700)
        self.console.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.initialize()

    def initialize(self):
        """
        Initializes the GUI components and starts the main loop.
        """
        self.setup_appearance()
        self.create_gui()
        self.root.mainloop()

    def set_appearance_mode(self, new_appearance_mode: str):
        """
        Sets the appearance mode of the application.

        Args:
            new_appearance_mode (str): The new appearance mode.
        """
        ctk.set_appearance_mode(new_appearance_mode)

    def setup_appearance(self):
        """
        Sets up the initial appearance of the application.
        """
        ctk.set_appearance_mode(self.DEFAULT_APPEARANCE)
        ctk.set_default_color_theme(self.DEFAULT_COLOR_THEME)

    def create_gui(self):
        """
        Creates the main GUI components.
        """
        self.root.geometry(self.DEFAULT_GEOMETRY)
        self.root.title("Integrity Check HIDS")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)

        self.create_sidebar()

    def create_sidebar(self):
        """
        Creates the sidebar components.
        """
        sidebar_frame = ctk.CTkFrame(self.root, width=140, corner_radius=0, border_color="Red")
        sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebar_frame.grid_rowconfigure(1, weight=1)

        self.tabview = ctk.CTkTabview(sidebar_frame, width=300, height=700)
        self.tabview.grid(padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Log History")
        self.tabview.add("Integrity Verification")

        self.create_log_buttons()
        self.create_check_integrity_buttons()
        self.create_appearance_options(sidebar_frame)

    def create_appearance_options(self, parent_frame: Frame) -> None:
        """
        Creates the appearance options in the sidebar.

        Args:
            parent_frame (Frame): The parent frame for the appearance options.
        """
        appearance_mode_label = ctk.CTkLabel(parent_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionmenu = ctk.CTkOptionMenu(parent_frame, values=self.VALUES_APPEARANCE,
                                                       command=self.change_appearance_mode_event)
        appearance_mode_optionmenu.grid(row=1, column=0, padx=20, pady=(10, 10))

    def create_log_buttons(self):
        """
        Creates buttons for log history.
        """
        frame = self.tabview.tab("Log History")
        logs_frame = ctk.CTkScrollableFrame(frame)
        logs_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        for index, name in enumerate(self.logs):
            log_button = ctk.CTkButton(logs_frame, text=name, fg_color="transparent",
                                       command=lambda file=name: self.display_output_logs(file))
            log_button.grid(row=index + 1, column=0, padx=10, sticky="w")

    def display_output_logs(self, file: str):
        """
        Displays log content in the console.

        Args:
            file (str): The selected log file.
        """
        for widget in self.console.winfo_children():
            widget.destroy()
        ruta_elemento = os.path.join("../logs", file)
        with open(ruta_elemento, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            title_label = ctk.CTkLabel(self.console, text=file,
                                       font=ctk.CTkFont(family=self.TERMINAL_FONT, size=20, weight="bold"))
            title_label.pack(side="top", anchor="w")
            contenido_label = ctk.CTkTextbox(self.console, width=2000, height=700,
                                           font=ctk.CTkFont(family=self.TERMINAL_FONT, size=15))
            contenido_label.pack(side="top", anchor="w")
            contenido_label.insert(ctk.END, contenido)

    def create_check_integrity_buttons(self):
        """
        Creates buttons for integrity verification.
        """
        frame = self.tabview.tab("Integrity Verification")

        files_frame = ctk.CTkScrollableFrame(frame)
        files_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        for index, name in enumerate(self.files):
            files_button = ctk.CTkButton(files_frame, text=name, fg_color="transparent",
                                         command=lambda file=name: self.display_output_files(file))
            files_button.grid(row=index + 1, column=0, padx=10, sticky="w")

    def display_output_files(self, file: str):
        """
        Displays file content and checks integrity.

        Args:
            file (str): The selected file for integrity check.
        """
        for widget in self.console.winfo_children():
            widget.destroy()
        title_label = ctk.CTkLabel(self.console, text=file,
                                   font=ctk.CTkFont(family=self.TERMINAL_FONT, size=20, weight="bold"))
        title_label.pack(side="top", anchor="w")
        contenido_label = ctk.CTkTextbox(self.console, width=2000, height=700,
                                       font=ctk.CTkFont(family=self.TERMINAL_FONT, size=15))
        contenido_label.pack(side="top", anchor="w")
        self.client.send_message(file)
        message = "Not Modified" if bool(self.client.receive_message()) else "Modified"
        contenido_label.insert(ctk.INSERT, message)

    def change_appearance_mode_event(self, mode: str) -> None:
        """
        Event handler for changing the appearance mode.

        Args:
            mode (str): The selected appearance mode.
        """
        self.set_appearance_mode(mode)
        ctk.set_appearance_mode(mode)

