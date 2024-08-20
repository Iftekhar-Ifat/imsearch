import customtkinter


class ThemeToggle(customtkinter.CTkButton):
    def __init__(self, master):
        super().__init__(master, text="Toggle Theme", command=self.toggle_theme)
        self.master = master
        self.pack(pady=20)

    def toggle_theme(self):
        if self.master.THEME == "dark":
            self.master.THEME = "light"
        else:
            self.master.THEME = "dark"
        customtkinter.set_appearance_mode(self.master.THEME)
