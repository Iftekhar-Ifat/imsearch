import customtkinter
from tkinter import filedialog


class DirectorySelector(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, width=400, height=150)
        self.pack_propagate(False)

        self.title_label = customtkinter.CTkLabel(
            self, text=title, font=("Inter", 16, "bold")
        )
        self.title_label.pack(pady=(10, 0))

        self.folder_path = None

        self.folder_label = customtkinter.CTkLabel(
            self, text="No directory selected", font=("Inter", 14)
        )
        self.folder_label.pack(pady=10, padx=10)

        self.folder_button = customtkinter.CTkButton(
            self, text="Select Directory", command=self.select_folder
        )
        self.folder_button.pack(pady=10, padx=10, side="bottom")

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.folder_label.configure(text=folder_path)
