import customtkinter
from .loading_spinner import LoadingSpinner


class InformationSection:
    def show_error_message(app):
        if not hasattr(app, "error_message") or not app.error_message:
            app.error_message = customtkinter.CTkLabel(
                app.information_section,
                text="Error: file or folder path not given",
                text_color="red",
                font=("Inter", 16),
            )
            app.error_message.pack(pady=(5, 0))

    def hide_error_message(app):
        if hasattr(app, "error_message") and app.error_message:
            app.error_message.pack_forget()

    def start_loading(app):
        app.loading = LoadingSpinner(
            app.information_section, size=(30, 30), isLoading=True
        )
        app.loading.pack(pady=(10, 0))

    def stop_loading(app):
        if hasattr(app, "loading") and app.loading:
            app.loading.pack_forget()

    def show_total_image(app, loaded_images):
        if hasattr(app, "total_images") and app.total_images:
            app.total_images.pack_forget()

        app.total_images = customtkinter.CTkLabel(
            app.information_section,
            text=f"Total Images: {len(loaded_images)}",
            font=("Inter", 16),
        )
        app.total_images.pack()

    def show_selected_model(app, selected_model):
        if hasattr(app, "selected_model") and app.selected_model:
            app.selected_model.pack_forget()

        app.selected_model = customtkinter.CTkLabel(
            app.information_section,
            text=f"Selected Model: {selected_model}",
            font=("Inter", 16),
        )
        app.selected_model.pack()
