import tkinter as tk
from tkinter import N, S, W, E
from player import MP3Player
from text_converter import TextConverter
from pdf_converter import PDFConverter
import styles as st
from resources import resource_path


class Interface:
    """
    Interface class is used to place the text_converter, pdf_converter, and player objects onto the master grid.

    Methods:
        __init__(self, master)
    """

    def __init__(self, master):
        """Interface class constructor to initialize the object.

        Input Arguments: parent must be Tk() object
        """

        # Setting up main window
        self.master = master
        self.master.title("PDF to MP3")
        self.icon = resource_path("images/favicon.ico")
        self.master.iconbitmap(self.icon)
        self.master.config(padx=10, pady=10)
        self.master.resizable(False, False)
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=0)

        # Initializing and placing Player
        self.mp3_player = MP3Player(master)
        self.mp3_player.grid(column=0, row=1, columnspan=2, stick=(W, S, E), padx=5, pady=5)

        # Initializing and placing PDF-Converter
        self.pdf_converter = PDFConverter(master, self.mp3_player)
        self.pdf_converter.grid(column=0, row=0, sticky=(N, W, S), padx=5, pady=5)

        # Initializing and placing Text-Converter
        self.text_converter = TextConverter(master, self.mp3_player)
        self.text_converter.grid(column=1, row=0, padx=5, pady=5)


# Final setup and run
root = tk.Tk()
root["background"] = st.BLUE
my_gui = Interface(root)
root.mainloop()


