import customtkinter as ctk
from .image_tile import ImageTile


class ResultSection(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1, minsize=820)

        # Title
        self.title = ctk.CTkLabel(
            self, text="Results", font=("Inter", 32, "bold"), anchor="w", justify="left"
        )
        self.title.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Subtitle
        self.subtitle = ctk.CTkLabel(
            self,
            text="Images are sorted by similarity",
            font=("Inter", 16, "italic"),
            anchor="w",
            justify="left",
        )
        self.subtitle.grid(row=1, column=0, sticky="w")

        # Results grid
        self.results_frame = ctk.CTkFrame(self, fg_color=("gray90", "#1F1F1F"))
        self.results_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.results_grid = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        self.results_grid.pack(fill="both", expand=True, padx=10, pady=10)

    def display_images(self, images):
        self.update_results(images)

    def create_image_grid(self, images):
        for i, img_name in enumerate(images):
            row = i // 5
            col = i % 5
            self.results_grid.grid_rowconfigure(row, weight=1)
            self.results_grid.grid_columnconfigure(col, weight=1)

            image_tile = ImageTile(self.results_grid, img_name)
            image_tile.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def update_results(self, new_img_arr):
        for widget in self.results_grid.winfo_children():
            widget.destroy()

        self.img_arr = new_img_arr
        self.create_image_grid(new_img_arr)
