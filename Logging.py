from datetime import datetime
import customtkinter as ctk


class Log:

    textBoxWidget: ctk.CTkTextbox = None

    @classmethod
    def log(cls, text: str, timeStamp=False, logFlag="|Info|", end="\n"):
        """Log text to both terminal and file.

        Args:
            LogFlag (str):  logging prefix flag. Can take one of the following values:  
                |Debug|; |Info|; |WARNING|; |ERROR|
            timeStamp (bool): choose whether terminal logging should include a timestamp.
                File logging will always include a timestamp.
        """

        cls.log_file(text, logFlag, end)
        cls.log_terminal(text, timeStamp, logFlag, end)
        cls.log_textbox(text, logFlag, end)

    @classmethod
    def log_terminal(cls, text: str, timeStamp=True, logFlag="|Info|", end="\n"):
        """Add a date and time stamp to the given text.
        Print text to terminal"""
        if timeStamp: print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}:", end="\t")
        print(f"{logFlag} {text}", end=end)

    @classmethod
    def log_file(cls, text: str, logFlag="|Info|", end="\n"):
        """Add a date and time stamp to the given text and 
        log it to a file."""
        file_path = f"Logs\\Log_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(file_path, "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}:")
            file.write(f"\t{logFlag} {text}{end}")
    
    @classmethod
    def log_textbox(cls, text: str, logFlag="|Info|", end="\n"):
        """Logs text to textbox widget with log flag."""
        Log.textBoxWidget.insert('0.0', f"{logFlag} {text}{end}")

    @classmethod
    def print(cls, text: str, end="\n"):
        """Logs plain text to textbox widget and console. No edits."""
        Log.textBoxWidget.insert('0.0', f"{text}{end}")
        print(text, end=end)
    
    @classmethod
    def set_textbox(cls, textbox: ctk.CTkTextbox):
        Log.textBoxWidget = textbox