import customtkinter
import threading
import gc
from ..utils.image_utils import GetImages
from .information_section import InformationSection
from ..imsearch import ImageSimilarity
from .result_section import ResultSection
from tkinter import messagebox


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
        self.after(0, self.process_info, loaded_images)

    def check_btn(self):
        self.file_path = self.app.upload_photo.file_path
        self.folder_path = self.app.directory_selector.folder_path
        queries = self._get_queries()

        self.restore_prev_state()

        if not self.file_path or not self.folder_path:
            messagebox.showerror(
                "Imsearch Error", "Error: File or folder path not given!"
            )
            return

        InformationSection.start_loading(self.app, size=(30, 30))
        self.enable_loading_state()

        self.selected_model = (
            "DINO" if queries.get("Quick Search") == "off" else "MOBILE_NET"
        )

        threading.Thread(
            target=self.load_images, args=(self.folder_path, queries), daemon=True
        ).start()

    def process_info(self, loaded_images):

        InformationSection.stop_loading(self.app)

        InformationSection.show_total_image(self.app, loaded_images)
        InformationSection.show_selected_model(self.app, self.selected_model)

        InformationSection.show_progress_bar(self.app)

        threading.Thread(
            target=self.search_images,
            args=(self.selected_model, self.file_path, loaded_images),
            daemon=True,
        ).start()

    def search_images(self, model_name, uploaded_image, image_array):
        try:
            with ImageSimilarity(model_name, image_array).memory_manager() as img_sim:
                total_image = len(image_array)

                if total_image == 0:
                    messagebox.showerror(
                        "Imsearch Error", "Error: Directory doesn't contain any images."
                    )
                    return

                # Search for similar images
                distances, indices, paths = img_sim.find_similar_images(
                    uploaded_image, k=total_image
                )

                ResultSection.display_images(self.app.result_section, images=paths)
                self.after(0, self.show_result)

        except Exception as e:
            messagebox.showerror("Imsearch Error", f"Error: {e}")
        finally:
            gc.collect()
            self.restore_prev_state()

    def show_result(self):
        self.app.result_section.pack()
        self.restore_prev_state()

    def restore_prev_state(self):
        InformationSection.hide_progress_bar(self.app)
        self.app.progress_bar = None
        self.configure(state="normal")
        self.configure(text="Check")

    def enable_loading_state(self):
        self.configure(text="Loading...")
        self.configure(state="disabled")
        InformationSection.hide_progress_bar(self.app)
