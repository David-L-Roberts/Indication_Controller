from ClientSocket import ClientSocket
from MsgGenerator import MsgGen

class SocketWriter():
    """Class for writing data to TCP socket.
    """
    def __init__(self, sock: ClientSocket) -> None:
        self._socket = sock

    def writeToSocket(self, dataBytes: bytes):
        """Writes given data to TCP Socket"""
        self._socket.setDataBytes(dataBytes)
        self._socket.sendData()

    def sendSlaveACK(self, addr: int):
        msgGen = MsgGen()
        msgGen.setDestAddress(addr)
        msgGen.setMessageType("FA")
        msgGen.generateMessage()
        self.writeToSocket(msgGen.getMessageAsBytes())