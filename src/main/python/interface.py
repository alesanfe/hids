import os
from tkinter import Frame

import customtkinter as ctk

from src.main.python.client import Client


class InterfaceHIDS:
    DEFAULT_GEOMETRY = "300x580"
    DEFAULT_APPEARANCE = "dark"
    DEFAULT_COLOR_THEME = "blue"
    VALUES_APPEARANCE = ["Dark", "Light"]
    TERMINAL_FONT = "Consolas"

    def __init__(self, host, port) -> None:
        """
        Initializes the InterfaceHIDS class.

        Args:
            host (str): Hostname or IP address of the server.
            port (int): Port number to establish a connection.
        """
        self.root = ctk.CTk()
        self.client = Client(host, port)
        self.client.connect()

        self.client.send_message("all_logs")
        self.logs = self.client.receive_message().split("|")

        self.client.send_message("all_files")
        self.files = self.client.receive_message().split("|")

        #self.console = ctk.CTkScrollableFrame(self.root, width=300, height=700)
        #self.console.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

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
        # self.root.geometry(self.DEFAULT_GEOMETRY)
        self.root.title("Integrity Check HIDS")

        #self.root.grid_columnconfigure(1, weight=1)
        #self.root.grid_columnconfigure((2, 3), weight=0)
        #self.root.grid_rowconfigure((0, 1, 2), weight=1)

        self.create_sidebar()

    def create_sidebar(self):
        """
        Creates the sidebar components.
        """
        sidebar_frame = ctk.CTkFrame(self.root,  corner_radius=0, border_color="Red")
        sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebar_frame.grid_rowconfigure(1, weight=1)

        self.tabview = ctk.CTkTabview(sidebar_frame)
        self.tabview.grid(padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Log History")
        self.tabview.add("Integrity Verification")

        self.create_log_buttons()
        self.create_check_integrity_buttons()


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
        log_window = ctk.CTkToplevel()
        # log_window.geometry(self.DEFAULT_GEOMETRY)



        os.path.join("../logs", file)
        self.client.send_message(f"log {file}")

        contenido = self.client.receive_message()
        title_label = ctk.CTkLabel(log_window, text=file,
                                       font=ctk.CTkFont(family=self.TERMINAL_FONT, size=20, weight="bold"))
        title_label.pack(side="top", anchor="w")
        content_label = ctk.CTkTextbox(log_window, width=1000, height=700,
                                           font=ctk.CTkFont(family=self.TERMINAL_FONT, size=15))
        content_label.pack(side="top", anchor="w")
        content_label.insert(ctk.END, contenido)

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
        file_frame = ctk.CTkToplevel()
        # file_frame.geometry(self.DEFAULT_GEOMETRY)

        self.client.send_message(f"file {file}")
        message = self.client.receive_message()

        message = "Not Modified" if message == "False" else "Modified"


        title_label = ctk.CTkLabel(file_frame, text=file,
                                   font=ctk.CTkFont(family=self.TERMINAL_FONT, size=20, weight="bold"))
        title_label.pack(side="top", anchor="w")

        content_label = ctk.CTkTextbox(file_frame, width=1000, height=700,
                                       font=ctk.CTkFont(family=self.TERMINAL_FONT, size=15))
        content_label.pack(side="top", anchor="w")

        content_label.insert(ctk.INSERT, message)


