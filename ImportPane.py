import customtkinter as ctk
from MessagePane import MessagePane
from Logging import Log
from os import getcwd

class ImportPane(MessagePane):
    def __init__(self, root: ctk.CTk, settings: dict, 
                 row=0, column=1, loadWidget: bool = True) -> None:
        super().__init__(root, row, column, loadWidget)

        self.csvPath = settings["csvFolder"]
        self.fileNameLabels: list[ctk.CTkLabel] = []
        # add sub widgets to the base frame
        self._add_frame_title("Import CSV of Indications")
        self.__add_selectFile_section()
        self.__add_uploadData_section()
    
    def append_fileNameLabel(self, label: ctk.CTkLabel):
        self.fileNameLabels.append(label)

    # -------------------------------------------------------------------------
    def __add_selectFile_section(self):
        self.selectFile_frame = ctk.CTkFrame(self.baseFrame)
        self.selectFile_frame.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.selectFile_frame.grid_columnconfigure((0, 1), weight=1)

        self.selectFile_label = ctk.CTkLabel(
            master=self.selectFile_frame,
            text="Select File",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.selectFile_label.grid(row=0, column=0, pady=(5, 5), columnspan=2)

        self.selectFile_button = ctk.CTkButton(
            master=self.selectFile_frame,
            text="Browse for CSV",
            command=self.__selectFile_button_event
        )
        self.selectFile_button.grid(row=1, column=0, padx=(20, 10), pady=(0, 5), sticky="e")

        self.refreshFile_button = ctk.CTkButton(
            master=self.selectFile_frame,
            text="Reload",
            command=self.__refreshFile_button_event
        )
        self.refreshFile_button.grid(row=1, column=1, padx=(10, 20), pady=(0, 5), sticky="w")

        self.filename_label = ctk.CTkLabel(
            master=self.selectFile_frame,
            text="no file selected...",
            font=ctk.CTkFont(size=12, weight="normal")
        )
        self.filename_label.grid(row=2, column=0, pady=(0, 5), columnspan=2)
        self.append_fileNameLabel(self.filename_label)

    def __selectFile_button_event(self):
        # ask user to select csv file (open file explorer). get file path
        self.filepath = ctk.filedialog.askopenfilename(
            # initialdir=getcwd() + "\\" + self.csvPath,
            title = "Select a CSV File",
            filetypes= [("CSV files", ["*.csv", "*.xlsx"]), ("Excel files", "*.xlsx"), ("All Files", "*.*")]
        )
        if self.filepath == "":
            Log.print("No file selected.")
            return
        
        self.import_csv(self.filepath)
    
    def import_csv(self, filepath):
        self.filename: str = filepath.split("/")[-1]             # get name of file
        Log.log(f"File ({self.filename}) imported successfully.")

        fileExtension = self.filename.split(".")[-1]

        # import selected file as a dataframe
        if fileExtension == "xlsx":
            self._excel_to_dataframe(filepath)
        else:
            self._csv_to_dataframe(filepath)

        # convert contents of df to message data format
        self._dataframe_to_messageData(MessagePane.csvDF)
      
        # update UI with name of file
        for label in self.fileNameLabels:
            label.configure(text=self.filename)

    
    def __refreshFile_button_event(self):
        if self.filepath == "":
            Log.print("No file has been selected.")
            return
        # import selected file as a dataframe
        self._excel_to_dataframe(self.filepath)
        # convert contents of df to message data format
        self._dataframe_to_messageData(MessagePane.csvDF)
    
        Log.log(f"File ({self.filename}) refresh success.")
        
    # -------------------------------------------------------------------------
    def __add_uploadData_section(self):
        self.uploadData_frame = ctk.CTkFrame(self.baseFrame)
        self.uploadData_frame.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.uploadData_frame.grid_columnconfigure(0, weight=1)

        self.uploadData_label = ctk.CTkLabel(
            master=self.uploadData_frame,
            text="Upload Data to RTU",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.uploadData_label.grid(row=0, column=0, pady=(5, 5))

        self.upload_button = ctk.CTkButton(
            master=self.uploadData_frame,
            text="Upload",
            command=self.__upload_button_event
        )
        self.upload_button.grid(row=1, column=0, padx=(20, 20), pady=(0, 20))


    def __upload_button_event(self):
        self._send_message()
        Log.log("Data upload in progress...")