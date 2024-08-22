import os
import glob
from tkinter import messagebox


class GetImages:
    def __init__(self, directory, extensions=("*.jpg", "*.jpeg", "*.png")):
        self.directory = directory
        self.extensions = extensions

    def get_images(self):
        images = []
        for ext in self.extensions:
            images.extend(glob.glob(os.path.join(self.directory, ext)))
        return images

    def get_nested_images(self):
        images = []
        for root, _, _ in os.walk(self.directory):
            for ext in self.extensions:
                images.extend(glob.glob(os.path.join(root, ext)))
        return images


def open_file(image_path):
    # Check if the provided image path exists
    if os.path.exists(image_path):
        try:
            if os.name == "nt":  # For Windows
                os.startfile(image_path)
            elif os.name == "posix":  # For Linux, MacOS
                subprocess.run(["xdg-open", image_path])
            else:
                messagebox.showerror("Error", "Unsupported operating system.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
    else:
        messagebox.showerror("Error", "File does not exist.")
