
class MessageData():
    """Class to hold data of a message"""
    def __init__(self) -> None:
        self._messageTypeCodeByte: bytes = b''  # action code, in byte form
        self._messageTypeCodeStr: str = ""      # action code, in string form
        self._messageTypeName: str = ""         # name of action code
    
        self._destAdress: bytes = b''   # RTU address to send message to (0-255)
        self._data: bytes = b''     # Data bytes of message
        self._crcCode: bytes = b''  # crc code of message

        self._message: bytes = b''  # total message frame to be sent

    def getMessageTypeName(self) -> str:
        """Return the name of the message type."""
        return self._messageTypeName
    
    def getMessageAsString(self) -> str:
        """Return the current message frame as a string."""
        messageString: str = "" 
        if self._message:
            for byte in self._message:
                byteFormatted = hex(byte)[2:].upper()
                if len(byteFormatted) < 2:
                    byteFormatted = "0" + byteFormatted
                messageString += byteFormatted + " "
        return messageString

    def getMessageAsBytes(self) -> bytes:
        """Return the current message frame as a byte array."""
        return self._message
    
    def _getDataAsString(self) -> str:
        """Return the current data bytes as a string."""
        dataString: str = "" 
        if self._data:
            for byte in self._data:
                byteFormatted = hex(byte)[2:].upper()
                if len(byteFormatted) < 2:
                    byteFormatted = "0" + byteFormatted
                dataString += byteFormatted + " "
        return dataString

    def _getDestAdressAsString(self) -> str:
        """Return the current destination address as a string."""
        addressString: str = "" 
        if self._destAdress:
            for byte in self._destAdress:
                byteFormatted = hex(byte)[2:].upper()
                if len(byteFormatted) < 2:
                    byteFormatted = "0" + byteFormatted
                addressString += byteFormatted + " "
        return addressString