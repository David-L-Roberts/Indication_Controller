import customtkinter as ctk

class SettingsPane:
    """settings page"""

    def __init__(self, root: ctk.CTk, row=0, column=1, loadWidget: bool = True) -> None:
        self.root = root
        self.row = row
        self.col = column

        # base frame for holding all settings widgets
        self.baseFrame = ctk.CTkFrame(master=self.root, width=600)
        self.loadPane()
        self.baseFrame.grid_columnconfigure(0, weight=1)
        # self.baseFrame.grid_rowconfigure(0, weight=1)

        # add sub widgets to the base frame
        self.__add_frame_title()
        self.__add_appearance_mode_optionMenu()
        # self.__add_color_mode_optionMenu()

        if not loadWidget:
            self.unloadPane()

    def loadPane(self):
        self.baseFrame.grid(row=self.row, column=self.col, padx=(20, 20), pady=(20, 20), sticky="nsew", columnspan=1)

    def unloadPane(self):
        self.baseFrame.grid_forget()
    
    def __add_frame_title(self,):
        self.title_label = ctk.CTkLabel(
            master=self.baseFrame,
            text="Settings",
            font=ctk.CTkFont(size=25, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="nsew" , columnspan=1)

    def __add_appearance_mode_optionMenu(self):
        self.appearance_mode_label = ctk.CTkLabel(
            self.baseFrame, 
            text="Appearance Mode:",
            font=ctk.CTkFont(size=16, weight="bold")
            )
        self.appearance_mode_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optioneMenu = ctk.CTkOptionMenu(
            self.baseFrame, 
            values=["Light", "Dark", "System"],
            command=self.__change_appearance_mode_event
        )
        self.appearance_mode_optioneMenu.set("Light")
        self.appearance_mode_optioneMenu.grid(row=3, column=0, padx=20, pady=(10, 10))    

    def __change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def __add_color_mode_optionMenu(self):
        self.color_mode_label = ctk.CTkLabel(
            self.baseFrame, 
            text="Color Mode:",
            font=ctk.CTkFont(size=16, weight="bold")
            )
        self.color_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0))

        self.color_mode_optionemenu = ctk.CTkOptionMenu(
            self.baseFrame, 
            values=["blue", "green", "dark-blue"],
            command=self.__change_color_mode_event 
        )
        self.color_mode_optionemenu.set("green")
        self.color_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))    

    def __change_color_mode_event(self, new_color_mode: str):
        ctk.set_default_color_theme(new_color_mode)
        print(new_color_mode)