import customtkinter
import threading
from ..utils.image_utils import GetImages
from .information_section import InformationSection


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

    def _get_queries(self):
        return {
            query.cget("text"): query.checkbox_state.get() for query in self.queries
        }

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
        queries = self._get_queries()

        if not self.file_path or not self.folder_path:
            InformationSection.show_error_message(self.app)
            return
        else:
            InformationSection.hide_error_message(self.app)

        InformationSection.start_loading(self.app, size=(30, 30))
        self.configure(state="disabled")

        self.selected_model = (
            "DINO" if queries.get("Quick Search") == "off" else "MOBILE_NET"
        )

        threading.Thread(
            target=self.load_images, args=(self.folder_path, queries), daemon=True
        ).start()

    def process_results(self, loaded_images):

        InformationSection.stop_loading(self.app)

        InformationSection.show_total_image(self.app, loaded_images)
        InformationSection.show_selected_model(self.app, self.selected_model)

        InformationSection.show_progress_bar(self.app)
