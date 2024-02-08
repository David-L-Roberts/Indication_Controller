import customtkinter as ctk
from MessagePane import MessagePane
from Logging import Log
from os import getcwd
from datetime import datetime
from tkinter.filedialog import asksaveasfile


class ExportPane(MessagePane):
    def __init__(self, root: ctk.CTk, row=0, column=1, loadWidget: bool = True) -> None:
        super().__init__(root, row, column, loadWidget)
        self.messageData.setMessageType("FD")

        # add sub widgets to the base frame
        self._add_frame_title("Export Indications to CSV")
        self.__add_selectFile_section()
        self.__add_saveFile_section()

    # -------------------------------------------------------------------------
    def __add_selectFile_section(self):
        self.exportIND_frame = ctk.CTkFrame(self.baseFrame)
        self.exportIND_frame.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.exportIND_frame.grid_columnconfigure(0, weight=1)

        self.exportIND_label = ctk.CTkLabel(
            master=self.exportIND_frame,
            text="Download Indications from RTU",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.exportIND_label.grid(row=0, column=0, pady=(5, 5))

        self.exportIND_button = ctk.CTkButton(
            master=self.exportIND_frame,
            text="Download",
            command=self.__importIND_button_event
        )
        self.exportIND_button.grid(row=1, column=0, padx=(20, 20), pady=(0, 5))

        self.exportStatus_label = ctk.CTkLabel(
            master=self.exportIND_frame,
            text="no data exported",
            font=ctk.CTkFont(size=12, weight="normal")
        )
        self.exportStatus_label.grid(row=2, column=0, pady=(0, 5))

    def __importIND_button_event(self):
        pass
        self.exportStatus_label.configure(text=f"last donwload: {datetime.now().strftime('%H:%M:%S')}")
        Log.log("download successful")
    
    # -------------------------------------------------------------------------
    def __add_saveFile_section(self):
        self.saveFile_frame = ctk.CTkFrame(self.baseFrame)
        self.saveFile_frame.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.saveFile_frame.grid_columnconfigure(0, weight=1)

        self.saveFile_label = ctk.CTkLabel(
            master=self.saveFile_frame,
            text="Save Export",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.saveFile_label.grid(row=0, column=0, pady=(5, 5))

        self.saveFile_button = ctk.CTkButton(
            master=self.saveFile_frame,
            text="Save As",
            command=self.__saveFile_button_event
        )
        self.saveFile_button.grid(row=1, column=0, padx=(20, 20), pady=(0, 20))


    def __saveFile_button_event(self):
        file = asksaveasfile(
            initialfile=f"RTU_export-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv",
            initialdir=getcwd(),
            defaultextension=".csv",
            filetypes=[("csv files", "*.csv")]
        )
        if file is None:
            Log.log("File not saved.")
            return

        file.close()
        Log.log("File saved successfully.")


        
        
            
            
    
