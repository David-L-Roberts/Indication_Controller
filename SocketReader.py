from threading import Thread, Event
from MessageLib import msgTypeLookup
from ClientSocket import ClientSocket
import time
from Logging import Log


class SocketReader():
    """   
    Starts a thread that will read data from TCP socket.
    Will read for `maxWaitsec` time, then sleep. Will wake when `readFromSocket` method is called.
    """
    def __init__(self, sock: ClientSocket, maxWaitSec: float=3) -> None:
        self._socket = sock
        self._currentMessageStr: str = ""
        self._currentMessageBytes: bytes = b''
        self.maxWaitSec = maxWaitSec

        self._event = Event()
        self._readThread = Thread(target=self.__threadLoop, daemon=True)
        self._readThread.start()

    def readFromSocket(self):
        """Start thread to read data from TCP socket."""
        self._event.set()
    
    def __threadLoop(self):
        while True:
            if self._event.is_set():
                self.__readFromSocket()
                self._event.clear()
            else:
                time.sleep(0.1)

    def __readFromSocket(self):
        """Try reading data from socket."""
        self._currentMessageBytes = b''
        endTime = time.time() + self.maxWaitSec

        while (endTime > time.time()):
            self._currentMessageBytes += self._socket.receiveData(timeoutSec=1)
            if b'\xF6' in self._currentMessageBytes: break # look for termination character (0xF6)

        self.__generateStrMessage()
        if self._currentMessageStr == "":
            Log.log(f"No Data Recieved after {self.maxWaitSec} sec", logFlag="|WARNING|")
        else:
            Log.log(f"Rx Data: {self._currentMessageStr}")
            Log.log(f"Rx Message Type: {self.getMessageType()}")

    def __generateStrMessage(self):
        self._currentMessageStr = ""

        for byte in self._currentMessageBytes:
                byteFormatted: str = hex(byte)[2:].upper()
                if len(byteFormatted) < 2:
                    byteFormatted = "0" + byteFormatted
                self._currentMessageStr += byteFormatted + " "

    def getMessageType(self):
        """Return the message type of the last read message."""
        try:
            controlCode = self._currentMessageStr[:2]
        except:
            messageType = None
            Log.log("No message recieved.", logFlag="|Debug|")
        else:
            try:
                messageType = msgTypeLookup[controlCode]
            except:
                messageType = controlCode
                Log.log("Received invalid Control Code.", logFlag="|ERROR|")

        return messageType
