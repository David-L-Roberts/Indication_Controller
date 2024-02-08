import socket
import selectors


class ClientSocket(socket.socket):
    def __init__(self, serverAddress) -> None:
        super().__init__(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.settimeout(5)

        self.__messageStr: str = "FB 05 F6"
        self.__messageBytes: bytes = bytes.fromhex(self.__messageStr)

        # connect local socket to TCP server
        print(f"Attempting to connect to server: {serverAddress[0]}, on port: {serverAddress[1]}")
        try:
            self.connect(serverAddress)
        except:
            raise Exception("Connection Failed! Server cannot be reached.")
        else:
            print("Success. Connected to Server: %s:%s" %self.getpeername()) 

        self.sel = selectors.DefaultSelector()
        # monitoredEvents = selectors.EVENT_READ | selectors.EVENT_WRITE
        monitoredEvents = selectors.EVENT_READ
        self.sel.register(self, monitoredEvents, data=None)

        self.settimeout(0)


    def __exit__(self, *args):
        print("Closing I/O Selector.")
        self.sel.close()
        print("Closing Client Socket.")
        super().__exit__(args)


    def setDataStr(self, message_string: str):
        """Set the message data to be sent as a string.
            message_string = string of hex code pairs. eg. 'FB 06 F8'
        """
        self.__messageStr = message_string
        self.__messageBytes = bytes.fromhex(message_string)

    def setDataBytes(self, message_bytes: bytes):
        """Set the message data to be sent as bytes.   
            message_btyes = byte array of hex code pairs. eg. b'\\xFB\\x06\\xF8'
        """
        self.__messageBytes = message_bytes
        self.__messageStr = message_bytes.hex(" ").upper()

    def sendData(self):
        self.sendall(self.__messageBytes)
    
    def receiveData(self, timeoutSec: float=1.0) -> bytes:
        """Read data from socket if there is any available.

        Args:
            timeoutSec (float, optional): max time that read opertaion will block for. Defaults to 1.0.

        Returns:
            bytes: data read from socket
        """
        events = self.sel.select(timeout=timeoutSec)
        rxData: bytes = b''
        for key, mask in events:
            rxData = self.__read_from_connection(key, mask)
        return rxData

    def __read_from_connection(self, key: selectors.SelectorKey, mask) -> bytes:
        sock: socket.socket = key.fileobj
        if mask & selectors.EVENT_READ:
            recv_data: bytes = sock.recv(1024)
            if recv_data:
                return recv_data
            else:
                return b''





