import customtkinter


class Header(customtkinter.CTkFrame):
    def __init__(self, master, title, subtitle):
        super().__init__(master, fg_color="transparent")
        self.pack(pady=(10, 30))

        self.title_label = customtkinter.CTkLabel(
            self,
            text=title,
            font=("Inter", 48, "bold"),
        )
        self.title_label.pack(pady=5, padx=10)

        self.subtitle_label = customtkinter.CTkLabel(
            self,
            text=subtitle,
            font=("Inter", 16, "italic"),
        )
        self.subtitle_label.pack(padx=20)
