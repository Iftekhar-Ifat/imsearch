import customtkinter
from PIL import Image
import os
from tkinter import filedialog
from .utils.image_utils import GetImages


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


class UploadPhoto(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, width=400, height=300)
        self.pack_propagate(False)

        self.title_label = customtkinter.CTkLabel(
            self, text=title, font=("Inter", 16, "bold")
        )
        self.title_label.pack(pady=(10, 0))

        self.file_path = None
        self.image_label = customtkinter.CTkLabel(
            self, text="No image selected", font=("Inter", 14)
        )
        self.image_label.pack(pady=10, padx=10)

        self.upload_button = customtkinter.CTkButton(
            self, text="Upload Photo", command=self.upload_image
        )
        self.upload_button.pack(pady=20, padx=20, side="bottom")

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path and os.path.isfile(file_path):
            self.file_path = file_path
            self.display_image()

    def display_image(self):
        if self.file_path:
            image = Image.open(self.file_path)
            width, height = image.size
            max_size = (300, 170)

            # Calculate aspect ratio
            if width > max_size[0] or height > max_size[1]:
                ratio = min(max_size[0] / width, max_size[1] / height)
                width = int(width * ratio)
                height = int(height * ratio)

            photo = customtkinter.CTkImage(image, size=(width, height))
            self.image_label.configure(text="", image=photo)

        else:
            print("No image file selected.")


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


class QueryCheckbox(customtkinter.CTkCheckBox):
    def __init__(self, master, title, checkbox_state):
        self.checkbox_state = checkbox_state
        super().__init__(
            master,
            text=title,
            # command=self.checkbox_event,
            variable=checkbox_state,
            onvalue="on",
            offvalue="off",
        )


class CheckButton(customtkinter.CTkButton):
    def __init__(self, master, queries, app):
        super().__init__(
            master,
            text="Check",
            font=("Inter", 20, "bold"),
            width=400,
            height=70,
            command=self.test,
        )
        self.queries = queries
        self.app = app

    def test(self):
        file_path = self.app.upload_photo.file_path
        folder_path = self.app.directory_selector.folder_path
        queries = {
            query.cget("text"): query.checkbox_state.get() for query in self.queries
        }

        if not file_path or not folder_path:
            print("Error: file or folder path not given")
            return

        total_images = (
            GetImages(folder_path).get_images()
            if queries.get("Deep Check") == "off"
            else GetImages(folder_path).get_nested_images()
        )

        selected_model = (
            "DINO" if queries.get("Quick Search") == "off" else "MOBILE_NET"
        )

        print(f"Files: {len(total_images)}")
        print(f"Model: {selected_model}")
        print(f"File path: {file_path}")

        # Update the result labels in the app
        self.app.update_total_images(len(total_images))


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
