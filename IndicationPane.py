import customtkinter as ctk
from MessagePane import MessagePane
from Logging import Log

MAX_BITS = 512

class IndicationPane(MessagePane):
    def __init__(self, root: ctk.CTk, row=0, column=1, loadWidget: bool = True) -> None:
        super().__init__(root, row, column, loadWidget)

        # add sub widgets to the base frame
        self._add_frame_title("Set Individual Bits")
        self.__add_currentCSV_section()
        self.__add_setBit_section()
        self.__add_resetBit_section()

    # -------------------------------------------------------------------------
    def __add_currentCSV_section(self):
        self.currentCSV_frame = ctk.CTkFrame(self.baseFrame)
        self.currentCSV_frame.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.currentCSV_frame.grid_columnconfigure((0,1), weight=1)

        self.currentCSV_label = ctk.CTkLabel(
            master=self.currentCSV_frame,
            text="Current CSV in use:",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.currentCSV_label.grid(row=0, column=0, pady=(5, 0), columnspan=2)

        self.csvFile_label = ctk.CTkLabel(
            master=self.currentCSV_frame,
            text="None",
            font=ctk.CTkFont(size=12, weight="normal")
        )
        self.csvFile_label.grid(row=1, column=0, pady=(0, 5), columnspan=2)

    def update_csvSelection(self, fileName):
        self.csvFile_label.configure(text=fileName)
        
    # -------------------------------------------------------------------------
    def __add_setBit_section(self):
        self.setBit_frame = ctk.CTkFrame(self.baseFrame)
        self.setBit_frame.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.setBit_frame.grid_columnconfigure(0, weight=2)
        self.setBit_frame.grid_columnconfigure((1, 2), weight=1)

        self.setBit_label = ctk.CTkLabel(
            master=self.setBit_frame,
            text="Set IND bit",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.setBit_label.grid(row=0, column=0, pady=(5, 5), columnspan=3)

        self.setBit_entryBox = ctk.CTkEntry(
            master=self.setBit_frame,
            placeholder_text=f"1-{MAX_BITS}",
        )
        self.setBit_entryBox.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="e")
        self.setBit_entryBox.bind('<Return>', self.__setBit1_button_event)

        self.setBit1_button = ctk.CTkButton(
            master=self.setBit_frame,
            text="Set",
            command=self.__setBit1_button_event
        )
        self.setBit1_button.grid(row=1, column=1, padx=(5, 5), pady=(0, 10), sticky='w')

        self.resetBit1_button = ctk.CTkButton(
            master=self.setBit_frame,
            text="Reset",
            command=self.__resetBit1_button_event
        )
        self.resetBit1_button.grid(row=1, column=2, padx=(5, 10), pady=(0, 10), sticky='w')

    def __setBit1_button_event(self, event=None):
        # read IND bit
        dataStr: str = self.setBit_entryBox.get()
        try: 
            dataInt = int(dataStr) 
            if (dataInt > MAX_BITS) or (dataInt < 1):
                raise Exception()
        except:
            Log.log(f"Invalid IND Bit number. Enter integer from 1-{MAX_BITS}.", logFlag="|ERROR|")
            self.setBit_entryBox.delete('0', 'end')
        else:
            # set data bit
            self.__update_dataFrame_val(dataInt, 1)
            # update message data
            self.__generate_byteData(dataInt)

            # send message
            self.messageData.generateMessage()
            self._send_message()
    
    def __resetBit1_button_event(self, event=None):
        # read IND bit
        dataStr: str = self.setBit_entryBox.get()
        try: 
            dataInt = int(dataStr) 
            if (dataInt > MAX_BITS) or (dataInt < 1):
                raise Exception()
        except:
            Log.log(f"Invalid IND Bit number. Enter integer from 1-{MAX_BITS}.", logFlag="|ERROR|")
            self.setBit_entryBox.delete('0', 'end')
        else:
            # reset data bit
            self.__update_dataFrame_val(dataInt, 0)
            # update message data
            self.__generate_byteData(dataInt)

            # send message
            self.messageData.generateMessage()
            self._send_message()
    
    def __update_dataFrame_val(self, bitNum: int, val: int):
        """Take a bitlist number and update the corresponding df entry with the new val

        Args:
            bitNum (int): bit list number to change
            val (int): either `0` or `1`
        """
        MessagePane.csvDF.loc[bitNum-1, ["Value"]] = val
    
    def __generate_byteData(self, bitNum):
        """Take a bitlist number and generate a bytecode pair for the corresponding bitlist byte.
        Updates the message payload with this bytecode pair.
        """
        byteNum: int = int(MessagePane.csvDF.loc[bitNum-1, ["Byte Num"]])
        self._dataframe_byte_to_messagedata(df=MessagePane.csvDF, byteNum=byteNum)
        

    # -------------------------------------------------------------------------
    def __add_resetBit_section(self):
        self.resetBit_frame = ctk.CTkFrame(self.baseFrame)
        self.resetBit_frame.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.resetBit_frame.grid_columnconfigure(0, weight=1)

        self.resetBit_label = ctk.CTkLabel(
            master=self.resetBit_frame,
            text="Reset IND bit",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.resetBit_label.grid(row=0, column=0, pady=(5, 5), columnspan=3)

        self.resetBit_entryBox = ctk.CTkEntry(
            master=self.resetBit_frame,
            placeholder_text=f"1-{MAX_BITS}",
        )
        self.resetBit_entryBox.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="e")
        self.resetBit_entryBox.bind('<Return>', self.__resetBit2_button_event)

        self.setBit2_button = ctk.CTkButton(
            master=self.resetBit_frame,
            text="Set",
            command=self.__setBit2_button_event
        )
        self.setBit2_button.grid(row=1, column=1, padx=(5, 5), pady=(0, 10), sticky='w')

        self.resetBit2_button = ctk.CTkButton(
            master=self.resetBit_frame,
            text="Reset",
            command=self.__resetBit2_button_event
        )
        self.resetBit2_button.grid(row=1, column=2, padx=(5, 10), pady=(0, 10), sticky='w')

    def __resetBit2_button_event(self, event=None):
        # read IND bit
        dataStr: str = self.resetBit_entryBox.get()
        try: 
            dataInt = int(dataStr) 
            if (dataInt > MAX_BITS) or (dataInt < 1):
                raise Exception()
        except:
            Log.log(f"Invalid IND Bit number. Enter integer from 1-{MAX_BITS}.", logFlag="|ERROR|")
            self.resetBit_entryBox.delete('0', 'end')
        else:
            # reset data bit
            self.__update_dataFrame_val(dataInt, 0)
            # update message data
            self.__generate_byteData(dataInt)

            # send message
            self.messageData.generateMessage()
            self._send_message()
    
    def __setBit2_button_event(self, event=None):
        # read IND bit
        dataStr: str = self.resetBit_entryBox.get()
        try: 
            dataInt = int(dataStr) 
            if (dataInt > MAX_BITS) or (dataInt < 1):
                raise Exception()
        except:
            Log.log(f"Invalid IND Bit number. Enter integer from 1-{MAX_BITS}.", logFlag="|ERROR|")
            self.resetBit_entryBox.delete('0', 'end')
        else:
            # set data bit
            self.__update_dataFrame_val(dataInt, 1)
            # update message data
            self.__generate_byteData(dataInt)

            # send message
            self.messageData.generateMessage()
            self._send_message()