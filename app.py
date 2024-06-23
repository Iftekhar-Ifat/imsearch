import customtkinter
from src.widgets import (
    Header,
    CheckButton,
    DirectorySelector,
    UploadPhoto,
    QueryCheckbox,
    ThemeToggle,
)
import os

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

        # Main label
        self.main_frame = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent", bg_color="transparent"
        )
        self.main_frame.pack(fill="both", expand=True)

        # Heading Section
        self.header = Header(
            self.main_frame,
            title="Imsearch",
            subtitle="Upload, Compare, and Discover Similar Images Effortlessly",
        )
        self.header.pack()

        # Upload Section
        self.upload_section = customtkinter.CTkFrame(
            self.main_frame, fg_color="transparent"
        )
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

        # Query Checkbox Frame
        self.query_checkbox_frame = customtkinter.CTkFrame(
            self.directory_section_frame, fg_color="transparent"
        )
        self.query_checkbox_frame.pack()

        # Deep search checkbox
        self.deep_check = QueryCheckbox(
            self.query_checkbox_frame,
            title="Deep Check",
            checkbox_state=customtkinter.StringVar(value="off"),
        )
        self.deep_check.pack()

        # Quick search query checkbox
        self.quick_search = QueryCheckbox(
            self.query_checkbox_frame,
            title="Quick Search",
            checkbox_state=customtkinter.StringVar(value="off"),
        )
        self.quick_search.pack()

        # Check Button widget
        self.check_button = CheckButton(
            self.upload_section,
            self.upload_photo,
            self.directory_selector,
            queries=[self.deep_check, self.quick_search],
        )
        self.check_button.pack(side="bottom", padx=20)

        ThemeToggle(self).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
