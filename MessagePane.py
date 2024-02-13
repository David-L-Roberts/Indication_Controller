import customtkinter as ctk
from MsgGenerator import MsgGen
from SocketWriter import SocketWriter
from SocketReader import SocketReader
import pandas as pd
from Logging import Log
from Utils import SETTINGS

class MessagePane:
    """Base class for message construct widget."""
    # class attributes
    sockWriter: SocketWriter = None
    sockReader: SocketReader = None
    csvDF: pd.DataFrame = None

    def __init__(self, root: ctk.CTk, row=0, column=1, loadWidget: bool = True) -> None:
        messageType = "FC"

        self.root = root
        self.row = row
        self.col = column
        self.messageData = MsgGen()
        self.messageData.setMessageType(messageType)
        self.messageData.setDestAddress(SETTINGS["TargetGenAddr"])

        # base frame for holding all message pane widgets
        self.baseFrame = ctk.CTkFrame(master=self.root)
        self.baseFrame.grid(row=row, column=column, padx=(20, 10), pady=(20, 20), sticky="nsew")
        self.baseFrame.grid_columnconfigure(0, weight=1)
        # self.baseFrame.grid_rowconfigure(3, weight=1)

        if not loadWidget:
            self.unloadPane()

    @classmethod
    def setComFunctions(cls, sockWriter: SocketWriter, sockReader: SocketReader):
        MessagePane.sockWriter = sockWriter
        MessagePane.sockReader = sockReader

    def loadPane(self):
        self.baseFrame.grid(row=self.row, column=self.col, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def unloadPane(self):
        self.baseFrame.grid_forget()
    
    def _add_frame_title(self, title):
        self.title_label = ctk.CTkLabel(
            master=self.baseFrame,
            text=title,
            width=420,
            font=ctk.CTkFont(size=25, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="nsew" , columnspan=1)

    def _send_message(self):
        """Send the constructed message."""
        # write data to serial
        Log.print("---")
        MessagePane.sockWriter.writeToSocket(self.messageData.getMessageAsBytes())
        Log.log(f"Tx Data: {self.messageData.getMessageAsString()}")
        Log.log(f"Tx Message Type: {self.messageData.getMessageTypeName()}")

        # MessagePane.sockReader.readFromSocket()
    
    def _csv_to_dataframe(self, filepath):
        """Take a file path to an indication_csv, and open it into a dataframe.
        Also apply basic filtering to data.
        """
        MessagePane.csvDF = pd.read_csv(filepath)
        MessagePane.csvDF = MessagePane.csvDF[["Bit Num", "Byte Num", "Value"]]

    def _excel_to_dataframe(self, filepath):
        """Take a file path to an excel indication file, and open it into a dataframe.
        Also apply basic filtering to data.
        """
        with open(filepath, 'rb') as file:
            MessagePane.csvDF = pd.read_excel(file)
        MessagePane.csvDF = MessagePane.csvDF[["Bit Num", "Byte Num", "Value"]]

    def _dataframe_to_messageData(self, df: pd.DataFrame):
        """Converts data frame contents to a string of hex bytecodes.
        Lowest byte number appears first.
        Sets the message data to the hexcode string.

        Args:
            df (pd.DataFrame): dataframe of bit numbers, byte numbers, and bit values.
        """
        # convert df to hexcode pairs
        byteCodePairs: bytes = b''
        for byteNum in df["Byte Num"].unique():
            byteCodePairs += self.__get_df_bytecodePair(df, byteNum)
            
        # set hexcode pairs as the message data 
        self.messageData.setData(byteCodePairs)
        self.messageData.generateMessage()
    
    def _dataframe_byte_to_messagedata(self, df: pd.DataFrame, byteNum):
        """Converts a byte of the data frame contents to a string of hex bytecodes.
        Sets the message data to the hexcode string.

        Args:
            df (pd.DataFrame): dataframe of bit numbers, byte numbers, and bit values.
        """    
        # convert df to hexcode pairs
        byteCodePairs: bytes = b''
        byteCodePairs += self.__get_df_bytecodePair(df, byteNum)
            
        # set hexcode pairs as the message data 
        self.messageData.setData(byteCodePairs)
        self.messageData.generateMessage()
    
    def __get_df_bytecodePair(self, df: pd.DataFrame, byteNum: int):
        """Calculates and returns the byte code pair for a 
        byte number of the given dataframe.  
        Byte code pair is: 0xByteNumber 0xByteData

        Args:
            df (pd.DataFrame): dataframe of bit numbers, byte numbers, and bit values.
            byteNum (int): byte number of df to calculate byte code pair for.

        Returns:
            bytes: byte code pair (0xbyteNumber 0xByteData)
        """
        # access values of given byte number
        byteSeries = df[df["Byte Num"] == byteNum]["Value"].reset_index(drop=True).copy()
        # convert series to equivalent hexcode
        dataByteCode: bytes = int(''.join(str(i) for i in byteSeries)[::-1], 2).to_bytes(length=1, byteorder='big')

        # convert bytenumber to hexcode of RTU address
        byteNumCode: bytes = int((byteNum-1)).to_bytes(length=1, byteorder='big')
        return byteNumCode + dataByteCode

    # def temp(self, df: pd.DataFrame, byteNum: int):
    #     return int((byteNum-1)).to_bytes(length=1, byteorder='big') + int(''.join(str(i) for i in df[df["Byte Num"] == byteNum]["Value"].reset_index(drop=True).copy())[::-1], 2).to_bytes(length=1, byteorder='big')