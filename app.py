import customtkinter
from src.widgets import Header, CheckButton, DirectorySelector, UploadPhoto, ThemeToggle
import os
from tkinter import filedialog

customtkinter.set_default_color_theme(
    os.path.join(os.path.dirname(__file__), "src\\custom_theme.json")
)
customtkinter.set_appearance_mode("light")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")
        self.title("Imsearch")
        self.THEME = "light"
        self.configure(
            pady=20,
            padx=20,
        )
        # Heading Section
        self.header = Header(
            self,
            title="Imsearch",
            subtitle="Upload, Compare, and Discover Similar Images Effortlessly",
        )
        self.header.pack()

        # Upload Section
        self.upload_section = customtkinter.CTkFrame(self, fg_color="transparent")
        self.upload_section.pack()

        # UploadPhoto widget
        self.upload_photo = UploadPhoto(self.upload_section, title="Select an Image")
        self.upload_photo.pack(side="left", padx=20)

        # Upload Directory Section
        self.directory_section_frame = customtkinter.CTkFrame(
            self.upload_section, fg_color="transparent"
        )
        self.directory_section_frame.pack(padx=20)

        # Upload Directory widget
        self.directory_selector = DirectorySelector(
            self.directory_section_frame,
            title="Select Search Directory",
        )
        self.directory_selector.pack()

        # Check widget
        self.check_button = CheckButton(self.upload_section)
        self.check_button.pack(side="bottom")

        ThemeToggle(self).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
