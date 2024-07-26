import customtkinter
from PIL import Image, ImageTk
import os
from tkinter import filedialog
from .utils.image_utils import GetImages
from .utils.helper import rotate_image


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
            command=self.check_btn,
        )
        self.queries = queries
        self.app = app

    def show_error_message(self):
        if not hasattr(self.app, "error_message") or not self.app.error_message:
            self.app.error_message = customtkinter.CTkLabel(
                self.app.information_section,
                text="Error: file or folder path not given",
                text_color="red",
                font=("Inter", 16),
            )
            self.app.error_message.pack(pady=(5, 0))

    def hide_error_message(self):
        if hasattr(self.app, "error_message") and self.app.error_message:
            self.app.error_message.pack_forget()

    def start_loading(self):
        self.app.loading = LoadingSpinner(
            self.app.information_section, size=(30, 30), isLoading=True
        )
        self.app.loading.pack(pady=(10, 0))

    def stop_loading(self):
        self.app.loading.pack_forget()

    def check_btn(self):
        file_path = self.app.upload_photo.file_path
        folder_path = self.app.directory_selector.folder_path
        queries = {
            query.cget("text"): query.checkbox_state.get() for query in self.queries
        }

        if not file_path or not folder_path:
            self.show_error_message()
            return

        self.hide_error_message()
        self.start_loading()

        total_images = (
            GetImages(folder_path).get_images()
            if queries.get("Deep Check") == "off"
            else GetImages(folder_path).get_nested_images()
        )

        selected_model = (
            "DINO" if queries.get("Quick Search") == "off" else "MOBILE_NET"
        )

        self.stop_loading()
        # self.app.total_images.configure(text=f"Total Images: {len(total_images)}")

        print(f"Files: {len(total_images)}")
        print(f"Model: {selected_model}")
        print(f"File path: {file_path}")


class LoadingSpinner(customtkinter.CTkFrame):
    def __init__(self, master, size, isLoading):
        super().__init__(master, fg_color="transparent")
        self.size = size
        self.original_image = Image.open("assets\spinner.png")
        self.original_image = self.original_image.resize(self.size)
        self.image = ImageTk.PhotoImage(self.original_image)
        self.label = customtkinter.CTkLabel(self, image=self.image, text="")
        self.label.pack(expand=True)
        self.angle = 0
        self.animate = True
        self.isLoading = isLoading

        if self.isLoading:
            self.start_loading()
        else:
            self.stop_loading()

    def rotate(self):
        if self.animate:
            self.angle += 15
            rotated_image = rotate_image(self.original_image, self.angle)
            self.label.configure(image=rotated_image)
            self.label.image = rotated_image
            self.after(30, self.rotate)

    def start_loading(self):
        self.animate = True
        self.rotate()

    def stop_loading(self):
        self.animate = False


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
