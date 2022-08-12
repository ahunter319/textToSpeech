import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from gtts import gTTS
from PyPDF2 import PdfFileReader
import styles as st
from resources import resource_path, languages, contents


class PDFConverter(tk.Frame):
    """
    PDFConverter class is a tk.Frame used to convert a pdf to speech and save it as an mp3 using Google
    text-to-speech.

    Methods:
        __init__(self, parent, player)
        select_file(self)
        convert_pdf(self)
        get_tld_code(self)
    """

    def __init__(self, parent, player):
        super().__init__()
        """PDFConverter class constructor to initialize the object.

        Input Arguments: parent must be Tk() object, player is an object of Player class
        """

        # Passing parent and player objects
        self.parent = parent
        self.player = player

        # Initial attributes
        self.file_to_convert = ""
        self.options = languages
        self.lang_details = contents
        self.TLD = "com"
        self.CODE = "en"

        # Frame setup
        self["borderwidth"] = 2
        self["relief"] = "raised"
        self["background"] = st.GREY

        # Creating/Placing Label-widget
        tk.Label(self, text="PDF to MP3 Converter", background=st.GREY, fg=st.BLUE, font=st.FONT_BG).grid(column=0,
                                                                                                          row=1)
        # Creating/Placing Button-widget, calls select_file method
        self.open_btn = tk.Button(self, text="Select File", command=self.select_file)
        self.open_btn.grid(column=0, row=2, padx=5, pady=5)

        # Creating/Placing Label-widget for chosen pdf file path
        self.file_path = StringVar()
        self.file_path.set(">> ")
        self.file_label = tk.Label(self, textvariable=self.file_path, background="white")
        self.file_label.grid(column=0, row=3, padx=5, pady=5)

        # Creating/Placing Label and Option-Menu widgets for language/accent dropdown menu
        tk.Label(self, background=st.GREY, fg=st.WHITE, text="Choose your language and/or accent",
                 font=st.FONT_SM).grid(column=0, row=4, padx=5, pady=5)
        self.option_var = StringVar()
        self.option_var.set(self.options[0])
        self.dropdown_menu = tk.OptionMenu(self, self.option_var, *self.options)
        self.dropdown_menu.grid(column=0, row=5, padx=5, pady=5)

        # Creating/Placing Button-widget, calls convert_pdf method
        self.convert_btn = tk.Button(self, text="Convert", command=self.convert_pdf)
        self.convert_btn.grid(column=0, row=6, padx=5, pady=5)

    def select_file(self):
        """
        Selects the pdf to be converted by opening a file browser, checking for correct extension, and setting the
        file_to_convert attribute to the chosen file path. If choice is correct extension, the name of the file is
        displayed on the interface.
        """

        # Getting file path
        temp_dir = filedialog.askopenfilename(parent=self, initialdir="/", title="Select a file")

        # Checking file path/extension
        if temp_dir:
            if temp_dir[-3:] != "pdf":
                messagebox.showerror(title="Invalid file format", message="Please select a pdf to convert.")
                self.select_file()
            else:
                self.file_to_convert = temp_dir

                # get file name to show user on gui
                temp_items = temp_dir.split("/")
                temp_name = temp_items[len(temp_items) - 1]
                self.file_path.set(f">> {temp_name}")

    def convert_pdf(self):
        """
        Converts chosen pdf to speech by first extracting text from pdf and sending string to google text-to-speech api.
        Mp3 is saved and loaded to player object. If fail to load file, user will be prompted to try opening a different
        file.
        """

        # Resetting player
        self.player.reset_player()

        # Getting tld and code for chosen language from dropdown
        self.get_tld_code()

        # Converting pdf to speech using pdfreader and google text-to-speech
        if self.file_to_convert:
            try:
                with open(self.file_to_convert, 'rb') as temp:
                    reader = PdfFileReader(temp)
                    num_pages = reader.getNumPages()

                    final_contents = ""
                    # Extracting/cleaning text from pdf
                    for n in range(num_pages):
                        page = reader.getPage(n)
                        page_contents = page.extractText()
                        cleaned = page_contents.replace("\n", "")
                        final_contents = final_contents + f" {cleaned}"

            except FileNotFoundError:
                messagebox.showinfo(title="Error opening file",
                                    message="File could not be opened. Please select a valid file")

            # Converting extracted text to speech and saving to output.mp3
            messagebox.showinfo(title="Converting PDF", message="Converting pdf. This may take a while...")
            tts = gTTS(final_contents, tld=self.TLD, lang=self.CODE)
            out_path = resource_path("out/output.mp3")
            tts.save(out_path)

            # Loading mp3 to player object and turn off Welcome-message
            self.player.welcome_on = False
            self.player.load_music()
            messagebox.showinfo(title="Success", message="Successful conversion. Try it out bellow.")

        else:
            messagebox.showinfo(title="Error", message="You must select a file to convert!")

    def get_tld_code(self):
        """
        Sets the tld and code attributes for the language/accent selected in Option-Menu widget by looking up the
        selected language key in languages.json.
        """

        new_lang = self.option_var.get()
        self.TLD = self.lang_details[new_lang]["tld"]
        self.CODE = self.lang_details[new_lang]["code"]



