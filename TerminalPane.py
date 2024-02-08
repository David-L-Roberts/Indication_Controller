import customtkinter as ctk


class TerminalPane:
    """ Add a panel that contains a textbox for logging
    Tx and Rx data.
    Also provides a button to clear text in textbox.
    """
    def __init__(self, root: ctk.CTk, row=0, column=2) -> None:
        self.root = root
        self.row = row
        self.col = column

        # base frame for holding text logger and button
        self.baseFrame = ctk.CTkFrame(master=self.root)
        self.loadPane()
        self.baseFrame.grid_columnconfigure(0, weight=1)
        self.baseFrame.grid_rowconfigure(1, weight=1)

        # add widgets
        self.__add_headerLabel()
        self.__add_textbox()
        self.__add_button()
    
    def loadPane(self):
        self.baseFrame.grid(row=self.row, column=self.col, padx=(10, 20), pady=(20, 20), sticky="nsew")

    def unloadPane(self):
        self.baseFrame.grid_forget()

    def __add_headerLabel(self):
        self.title_label = ctk.CTkLabel(
            master=self.baseFrame,
            text="Comms Log",
            font=ctk.CTkFont(size=25, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="nsew" , columnspan=1)

    def __add_textbox(self):
        self.textbox = ctk.CTkTextbox(
            master=self.baseFrame,
            width=400,
            height=60,
            state="normal",
            font=ctk.CTkFont(size=14)
        )
        self.textbox.grid(
            row=1, 
            column=0, 
            padx=(10, 10), 
            pady=(10, 10), 
            sticky='nsew', 
            columnspan=1
        )
    
    def __add_button(self):
        self.button_clearText = ctk.CTkButton(
            master=self.baseFrame,
            text="Clear Text",
            command=self.__button_event
        )
        self.button_clearText.grid(row=2, column=0, padx=(10, 10), pady=(0, 10))

    def __button_event(self):
        self.textbox.delete('0.0', 'end')