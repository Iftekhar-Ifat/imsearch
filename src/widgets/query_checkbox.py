import customtkinter


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
