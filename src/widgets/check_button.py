import customtkinter
import threading
from ..utils.image_utils import GetImages
from .loading_spinner import LoadingSpinner


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

    def load_images(self, folder_path, queries):
        loaded_images = (
            GetImages(folder_path).get_images()
            if queries.get("Deep Check") == "off"
            else GetImages(folder_path).get_nested_images()
        )
        self.after(0, self.process_results, loaded_images)

    def check_btn(self):
        self.file_path = self.app.upload_photo.file_path
        self.folder_path = self.app.directory_selector.folder_path
        queries = {
            query.cget("text"): query.checkbox_state.get() for query in self.queries
        }

        if not self.file_path or not self.folder_path:
            self.show_error_message()
            return

        self.hide_error_message()
        self.start_loading()

        self.selected_model = (
            "DINO" if queries.get("Quick Search") == "off" else "MOBILE_NET"
        )

        threading.Thread(
            target=self.load_images, args=(self.folder_path, queries), daemon=True
        ).start()

    def process_results(self, loaded_images):
        self.stop_loading()
        print(f"Files: {len(loaded_images)}")
        print(f"Model: {self.selected_model}")
        print(f"File path: {self.file_path}")
