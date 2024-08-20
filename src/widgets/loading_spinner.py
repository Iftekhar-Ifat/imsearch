import customtkinter
from ..utils.helper import rotate_image
from PIL import Image, ImageTk


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
