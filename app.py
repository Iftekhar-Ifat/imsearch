import customtkinter
from src.widgets import Header, UploadPhoto, ThemeToggle
import os
from tkinter import filedialog

customtkinter.set_default_color_theme(
    os.path.join(os.path.dirname(__file__), "src\\custom_theme.json")
)
customtkinter.set_appearance_mode("light")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("CTk example")
        self.THEME = "light"
        self.configure(
            pady=20,
            padx=20,
        )

        # Initialize Header
        self.header = Header(
            self,
            title="Imsearch",
            subtitle="Upload, Compare, and Discover Similar Images Effortlessly",
        )
        self.header.pack()

        # Initialize UploadPhoto widget
        self.upload_photo = UploadPhoto(self)
        self.upload_photo.pack()

        ThemeToggle(self)


""" 
    def checkbox_event(self):
        print("checkbox toggled, current value:", self.widgets.check_var.get())

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path and os.path.isfile(file_path):
            print("Selected file:", file_path)
            self.widgets.display_image(file_path)

    def button_click(self):
        if self.THEME == "dark":
            self.THEME = "light"
        else:
            self.THEME = "dark"
            customtkinter.set_appearance_mode(self.THEME)
 """

if __name__ == "__main__":
    app = App()
    app.mainloop()
