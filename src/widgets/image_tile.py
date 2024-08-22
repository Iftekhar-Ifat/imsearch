import customtkinter as ctk
from PIL import Image
from ..utils.image_utils import open_file


class ImageTile(ctk.CTkFrame):
    def __init__(self, master, image_path):
        super().__init__(master, fg_color="gray80")
        self.image_path = image_path

        self.image_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.image_frame.pack(expand=True, fill="both")

        self.image_label = ctk.CTkLabel(
            self.image_frame,
        )
        self.image_label.pack(expand=True, fill="both")
        self.display_image(image_path)

        self.image_label.bind("<Double-Button-1>", self.on_double_click)

    def on_double_click(self, event):
        open_file(self.image_path)

    def display_image(self, image_path):
        if image_path:
            image = Image.open(image_path)
            width, height = image.size
            max_size = (150, 100)

            # Calculate aspect ratio
            if width > max_size[0] or height > max_size[1]:
                ratio = min(max_size[0] / width, max_size[1] / height)
                width = int(width * ratio)
                height = int(height * ratio)

            photo = ctk.CTkImage(image, size=(width, height))
            self.image_label.configure(text="", image=photo)

        else:
            print("No image file selected.")
