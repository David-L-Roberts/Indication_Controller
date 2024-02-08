import main as MAIN

def main():
    settings = MAIN.load_settings()
    serverAddress = ('localhost', settings["ServerPort"])

    with MAIN.ClientSocket(serverAddress) as sock: 
        root = MAIN.ctk.CTk()
        mainApp = MAIN.MainApp(
            root=root,
            tcpSocket=sock,
            readTimeoutSec=settings["ReadTimeoutSec"]
        )
        mainApp.root.mainloop()

if __name__ == "__main__":
    main()