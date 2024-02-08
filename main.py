import customtkinter as ctk
from ClientSocket import ClientSocket
from SocketWriter import SocketWriter
from SocketReader import SocketReader
from NavigationPanel import NavigationPanel
from MessagePane import MessagePane
from IndicationPane import IndicationPane
from ImportPane import ImportPane
from ExportPane import ExportPane
from TerminalPane import TerminalPane
from SetttingsPane import SettingsPane
from Utils import load_settings
from Logging import Log

ctk.set_appearance_mode("Light")         # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")     # Themes: "blue" (standard), "green", "dark-blue"


class MainApp:
    """
    """
    def __init__(self, root: ctk.CTk, tcpSocket: ClientSocket, settings: dict=None) -> None:
        # TCP client socket
        self.socket = tcpSocket
        self.socketWriter = SocketWriter(sock=self.socket)
        self.socketReader = SocketReader(sock=self.socket, maxWaitSec=settings["ReadTimeoutSec"])

        # GUI setup
        self.root = root
        self.configure_root()

        self.terminalPane = TerminalPane(self.root)
        Log.set_textbox(self.terminalPane.textbox)  # pass textbox widget to logger

        MessagePane.setComFunctions(self.socketWriter, self.socketReader) # pass comport objects to message panes
        self.indBit_pane    = IndicationPane(self.root, loadWidget=False)
        self.import_pane    = ImportPane(self.root, settings=settings, loadWidget=True)
        self.export_pane    = ExportPane(self.root, loadWidget=False)
        self.settingsPane   = SettingsPane(self.root, loadWidget= False)
        self.navigationPanel    = NavigationPanel(self, row=0, column=0)
        # allow imported filename to update on IND bit pane
        self.import_pane.append_fileNameLabel(self.indBit_pane.csvFile_label)   

        # default CSV import
        self.import_pane.import_csv(settings["DataTemplate"])



    def configure_root(self):
        self.root.title("Indication Controller")
        # self.root.geometry(f"{1115}x{600}")
        self.root.minsize(width=670, height=375)
        # self.root.maxsize(width=1115, height=1080)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.iconbitmap("resources\\CustomTkinter_logo_single.ico")


# ---------------------------- MAIN FUNCTION ------------------------------- #

def main():
    settings = load_settings()
    serverAddress = (settings["ServerIP"], settings["ServerPort"])

    with ClientSocket(serverAddress) as sock: 
        root = ctk.CTk()
        mainApp = MainApp(
            root=root,
            tcpSocket=sock,
            settings=settings
        )
        mainApp.root.mainloop()

if __name__ == "__main__":
    main()