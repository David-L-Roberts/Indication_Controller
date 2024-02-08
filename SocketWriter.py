from ClientSocket import ClientSocket

class SocketWriter():
    """Class for writing data to TCP socket.
    """
    def __init__(self, sock: ClientSocket) -> None:
        self._socket = sock

    def writeToSocket(self, dataBytes: bytes):
        """Writes given data to TCP Socket"""
        self._socket.setDataBytes(dataBytes)
        self._socket.sendData()

    