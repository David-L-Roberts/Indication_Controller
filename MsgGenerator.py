import crcmod
import customtkinter as ctk
from MessageData import MessageData
import MessageLib as msgLib
from Logging import Log

class MsgGen(MessageData):
    """Message Generator class.
    Provides the functions required to generate and format 
    a Genisys message for transmission.
    """
    def __init__(self) -> None:
        super().__init__()
        self.__setCrcFunction()

    def setMessageType(self, messageTypeCode: str):
        self._messageTypeCodeStr = messageTypeCode
        self._messageTypeName = msgLib.msgTypeLookup[messageTypeCode]
        self._messageTypeCodeByte = msgLib.masterMsgCodes[self._messageTypeName]
            
    def setDestAddress(self, addr: int):
        """set address bit of message.
        """
        self._destAdress: bytes = addr.to_bytes(length=1, byteorder='big')

    def setData(self, data: bytes):
        """take raw byte string to use as message data"""
        self._data = data

    def setDataBit(self, data: int):
        """Set data of message to be an individual bit.
        Data param is an integer corresponding to bit list num of IND.
        """
        self._data = self.__bitList_to_regByte(data)

    def __bitList_to_regByte(self, bitListNum):
        """Conver a bit list number to the corresponding RTU register byte pair."""
        byteNumInt: int = 0
        bitNumInt: int = 0

        byteNumInt = int(bitListNum/8)

        bitNumInt = bitListNum % 8
        if bitNumInt == 0:
            byteNumInt -= 1
            bitNumInt = 8
        bitNumInt = (0b01 << (bitNumInt - 1))

        bitNumByte: bytes = bitNumInt.to_bytes(length=1, byteorder='big')
        byteNumByte: bytes = byteNumInt.to_bytes(length=1, byteorder='big')

        return byteNumByte + bitNumByte

    def __setCrcFunction(self):
        """Generate a crc function for caculating a CRC-16 code."""
        crcPoly = 0x18005   #CRC polynomial
        self._crc16 = crcmod.mkCrcFun(
            poly=crcPoly,
            initCrc=0x0000,
            rev=True,
            xorOut=0x0000
        )

    def __generateCRC(self):
        """Generates a CRC code for the given data.
        Uses the 'CRC-16-IBM' algorithim, using the generator polynomial '0x8005'.
        """
        crcRaw: int = self._crc16(data=self._message)    # crc code - integer form
        crcBytes: bytes = crcRaw.to_bytes(length=2, byteorder='little') # crc code - byte form - LSB first
        self._crcCode: bytes = crcBytes

    def _addCRC(self):
        """Creates and appends a 16-bit CRC code to the end of the message.
        Will not append CRC if message is of type 'Poll'.
        """
        if self._messageTypeCodeStr == "FB":
            return
        
        self.__generateCRC()            # generate CRC code for the message
        self._message += self._crcCode  # append crc code
    
        
    def _addCharPadding(self):
        """Scan message for bytes equal to or greater than 0xF0.
        Replaces them with 2 bytes.
            ->  bytes are changed from 0xFn to 0xF0 0x0n.
        Does not replace the Control Character with a padded byte.
        """
        #ignore the first 'control character' byte when adding padding bytes
        newMessage = self._message[0].to_bytes(length=1, byteorder='big')
        # scan message for bytes greater or equal to 0xF0. Replace with padded byte pair
        for byte in self._message[1:]:
            if byte >= 0xF0:    # add a padded byte
                remainder = byte - 0xF0
                secondByte = remainder.to_bytes(length=1, byteorder='big')
                paddedByte = b'\xF0' + secondByte
                newMessage += paddedByte
            else:
                newMessage += byte.to_bytes(length=1, byteorder='big')
        self._message = newMessage


    def _addTerminator(self):
        """Adds the termination character to the end of the message."""
        self._message += b'\xF6'


    def generateMessage(self):
        """Generate the message frame with the given control code, destination address, 
        and (if revelavant) data bytes.
        Print the result to the message text box field.
        """
        # check that a destination address has been given
        if not self._destAdress:
            Log.log("No destination address has been provided.", logFlag="|ERROR|")
            return
        
        # generate message frame
        self._message = self._messageTypeCodeByte + self._destAdress + self._data
        self._addCRC()
        self._addCharPadding()
        self._addTerminator()



