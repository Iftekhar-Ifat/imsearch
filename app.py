import customtkinter
import os

from src.widgets import (
    Header,
    UploadPhoto,
    DirectorySelector,
    QueryCheckbox,
    ThemeToggle,
    CheckButton,
    ResultSection,
)

customtkinter.set_default_color_theme(
    os.path.join(os.path.dirname(__file__), "custom_theme.json")
)
customtkinter.set_appearance_mode("light")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")
        self.title("Imsearch")
        self.wm_iconbitmap("assets/imsearch.ico")
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
        self.query_checkbox_frame.pack(fill="both", expand=True, padx=30, pady=(5, 5))

        # Deep search checkbox
        self.deep_check = QueryCheckbox(
            self.query_checkbox_frame,
            title="Deep Check",
            checkbox_state=customtkinter.StringVar(value="off"),
        )
        self.deep_check.grid(row=0, column=0, padx=10, sticky="w")

        self.deep_check_description = customtkinter.CTkLabel(
            self.query_checkbox_frame,
            text="( Include Nested Folders )",
            fg_color="transparent",
        )
        self.deep_check_description.grid(row=0, column=2, pady=(5, 5), sticky="w")

        # Quick search query checkbox
        self.quick_search = QueryCheckbox(
            self.query_checkbox_frame,
            title="Quick Search",
            checkbox_state=customtkinter.StringVar(value="off"),
        )
        self.quick_search.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="w")

        self.quick_search_description = customtkinter.CTkLabel(
            self.query_checkbox_frame,
            text="( Faster Search )",
            fg_color="transparent",
        )
        self.quick_search_description.grid(row=1, column=2, sticky="w")

        # Check Button widget
        self.check_button = CheckButton(
            self.upload_section,
            queries=[self.deep_check, self.quick_search],
            app=self,
        )
        self.check_button.pack(side="bottom", padx=20)

        # Information Section
        self.information_section = customtkinter.CTkFrame(
            self.main_frame, fg_color="transparent"
        )
        self.information_section.pack(fill="both", expand=True, pady=(10, 0))

        # Result Section
        self.result_section = ResultSection(
            self.main_frame,
        )

        ThemeToggle(self).pack()

    def update_total_images(self, total):
        self.total_images.configure(text=f"Total Images: {total}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
