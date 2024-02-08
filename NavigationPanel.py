import customtkinter as ctk

class NavigationPanel:
    def __init__(self, master, row=0, column=0) -> None:

        self.master = master  # Main app object

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(master.root, corner_radius=0)
        self.navigation_frame.grid(row=row, column=column, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        # Side panel Title
        self.navigation_frame_label = ctk.CTkLabel(
            master=self.navigation_frame, 
            text="Menu", 
            compound="left",
            width=140,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # add side panel buttons
        self.ind_button = ctk.CTkButton(
            master=self.navigation_frame, 
            corner_radius=0, height=30, border_spacing=10, 
            text="Individual Bits",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", 
            command=self.ind_button_event
        )
        self.ind_button.grid(row=1, column=0, sticky="ew")

        self.import_button = ctk.CTkButton(
            master=self.navigation_frame, 
            corner_radius=0, height=30, border_spacing=10, 
            text="Import From CSV",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", 
            command=self.import_button_event
        )
        self.import_button.grid(row=2, column=0, sticky="ew")

        self.export_button = ctk.CTkButton(
            master=self.navigation_frame, 
            corner_radius=0, height=30, border_spacing=10, 
            text="Export to CSV (TBD)",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", 
            command=self.export_button_event
        )
        self.export_button.grid(row=3, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(
            master=self.navigation_frame, 
            text="Settings",
            command=self.settings_button_event
        )
        self.settings_button.grid(row=6, column=0)

        # set default page
        self.pageName = "Import"
        self.select_page()


    def ind_button_event(self):
        self.pageName = "Ind"
        self.select_page()

    def import_button_event(self):
        self.pageName = "Import"
        self.select_page()

    def export_button_event(self):
        self.pageName = "Export"
        self.select_page()


    def settings_button_event(self):
        self.pageName = "Settings"
        self.select_page()


    def select_page(self):
        # set button color for selected button
        name = self.pageName
        self.ind_button.configure(fg_color=("gray75", "gray25") if name == "Ind" else "transparent")
        self.import_button.configure(fg_color=("gray75", "gray25") if name == "Import" else "transparent")
        self.export_button.configure(fg_color=("gray75", "gray25") if name == "Export" else "transparent")

        # show selected frame
        if name == "Ind":
            self.master.indBit_pane.loadPane()
        else:
            self.master.indBit_pane.unloadPane()
        if name == "Import":
            self.master.import_pane.loadPane()
        else:
            self.master.import_pane.unloadPane()
        if name == "Export":
            self.master.export_pane.loadPane()
        else:
            self.master.export_pane.unloadPane()

        if name == "Settings":
            self.master.settingsPane.loadPane()
            self.master.terminalPane.unloadPane()
        else:
            self.master.settingsPane.unloadPane()
            self.master.terminalPane.loadPane()

