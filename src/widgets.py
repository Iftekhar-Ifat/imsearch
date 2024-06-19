import customtkinter
from PIL import Image
import os
from tkinter import filedialog


class Header(customtkinter.CTkFrame):
    def __init__(self, master, title, subtitle):
        super().__init__(master, fg_color="transparent")
        self.pack(pady=10)

        self.title_label = customtkinter.CTkLabel(
            self,
            text=title,
            font=("Inter", 32, "bold"),
        )
        self.title_label.pack(pady=5, padx=10)

        self.subtitle_label = customtkinter.CTkLabel(
            self,
            text=subtitle,
            font=("Inter", 16),
        )
        self.subtitle_label.pack(pady=5, padx=20)


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
        super().__init__(master, width=400, height=200)
        self.pack_propagate(False)

        self.title_label = customtkinter.CTkLabel(
            self, text=title, font=("Inter", 16, "bold")
        )
        self.title_label.pack(pady=(10, 0))

        self.folder_path = None

        self.folder_label = customtkinter.CTkLabel(
            self, text="No directory selected", font=("Inter", 14)
        )
        self.folder_label.pack(pady=30, padx=10)

        self.folder_button = customtkinter.CTkButton(
            self, text="Select Directory", command=self.select_folder
        )
        self.folder_button.pack(pady=20, padx=10, side="bottom")

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.folder_label.configure(text=folder_path)


class CheckButton(customtkinter.CTkButton):
    def __init__(self, master):
        super().__init__(
            master,
            text="Check",
            font=("Inter", 20, "bold"),
            width=400,
            height=70,
            command=self.test,
        )

    def test(self):
        print("hello")


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


"""         self.button = customtkinter.CTkButton(
            self.master, text="Toggle Theme", command=self.button_click
        )
        self.button.grid(row=0, column=0, padx=20, pady=10)
 """
"""     def button_click(self):
        if self.THEME == "dark":
            self.THEME = "light"
        else:
            self.THEME = "dark"
            customtkinter.set_appearance_mode(self.THEME)
 """


""" class Widgets:
    # def __init__(self):
    # self.theme_toggle()

    # self.master = master
    # self.button_click = button_click
    # self.checkbox_event = checkbox_event
    # self.upload_image = upload_image
    # self.create_widgets()

    def theme_toggle(self, button_click):
        self.button = customtkinter.CTkButton(
            self.master, text="Toggle Theme", command=button_click
        )
        self.button.grid(row=0, column=0, padx=20, pady=10)


    def create_widgets(self):
        self.button = customtkinter.CTkButton(
            self.master, text="Toggle Theme", command=self.button_click
        )
        self.button.grid(row=0, column=0, padx=20, pady=10)

        self.check_var = customtkinter.StringVar(value="on")

        self.checkbox = customtkinter.CTkCheckBox(
            self.master,
            text="CTkCheckBox",
            variable=self.check_var,
            command=self.checkbox_event,
            onvalue="on",
            offvalue="off",
        )
        self.checkbox.grid(row=1, column=0, padx=20, pady=10)

        img_path = os.path.join(os.path.dirname(__file__), "test_img.png")
        self.img = customtkinter.CTkImage(
            light_image=Image.open(img_path),
            dark_image=Image.open(img_path),
            size=(100, 100),
        )

        self.image_label = customtkinter.CTkLabel(
            self.master,
            image=self.img,
        )
        self.image_label.grid(row=2, column=0, padx=20, pady=10)

        self.upload_button = customtkinter.CTkButton(
            self.master, text="Upload Image", command=self.upload_image
        )
        self.upload_button.grid(row=3, column=0, padx=20, pady=10)

    def display_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
 """
