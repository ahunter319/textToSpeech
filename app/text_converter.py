import tkinter as tk
from tkinter import messagebox, StringVar
from gtts import gTTS
import styles as st
from resources import resource_path, languages, contents


class TextConverter(tk.Frame):
    """
    TextConverter class is a tk.Frame used to convert user-entered text inside a text-widget to speech using Google
    text-to-speech.

    Methods:
        __init__(self, parent, player)
        convert_text(self)
        clear_text(self)
        get_tld_code(self)
    """

    def __init__(self, parent, player):
        super().__init__()
        """TextConverter class constructor to initialize the object.
        
        Input Arguments: parent must be Tk() object, player is an object of Player class
        """

        # Initial attributes
        self.options = languages
        self.lang_details = contents
        self.TLD = "com"
        self.CODE = "en"

        # Passing parent and player objects
        self.parent = parent
        self.player = player

        # Frame setup
        self["borderwidth"] = 2
        self["relief"] = "raised"
        self["background"] = st.GREY
        tk.Label(self, text="Text to MP3 Converter", bg=st.GREY, fg=st.BLUE, font=st.FONT_BG).grid(column=0, row=0,
                                                                                                   columnspan=3)

        # Creating/Placing Text widget
        self.entered_text = tk.Text(self, height=12, width=50, wrap=tk.WORD, spacing2=6, padx=5, pady=5,
                                    font=st.FONT_SM)
        self.entered_text.grid(column=0, row=1, columnspan=3, padx=10)

        # Creating/Placing language/accent dropdown Option-menu widget
        self.option_var = StringVar()
        self.option_var.set(self.options[0])
        self.dropdown_menu = tk.OptionMenu(self, self.option_var, *self.options)
        self.dropdown_menu.grid(column=0, row=3, padx=5, pady=5)

        # Creating/Placing Button widget, calls convert_text method
        self.convert_text_btn = tk.Button(self, text="Convert", command=self.convert_text)
        self.convert_text_btn.grid(column=1, row=3, padx=5, pady=5)

        # Creating/Placing Button widget, calls clear_text method
        self.clear_text_btn = tk.Button(self, text="Clear", command=self.clear_text)
        self.clear_text_btn.grid(column=2, row=3, padx=5, pady=5)

    def convert_text(self):
        """
        Gets user-entered text from text-widget, passes text to google text-to-speech api through python gtts package,
        saves mp3 to output file, and loads it in mp3-player object. If user hasn't entered any text it will prompt them
        to type something through a tk messagebox.
        """

        # Getting user-entered text from Text-widget
        contents = self.entered_text.get("1.0", "end").strip()

        # Resetting mp3 player
        self.player.reset_player()

        # Getting language code/tld from Option-Menu widget
        self.get_tld_code()

        # Converting text
        if len(contents) > 0:
            tts = gTTS(contents, tld=self.TLD, lang=self.CODE)
            out_path = resource_path("out/output.mp3")
            tts.save(out_path)

            # Loading mp3 to player object and turn off Welcome-message
            self.player.welcome_on = False
            self.player.load_music()

            messagebox.showinfo(title="Success!", message="Text converted. Try listening in the player bellow!")
        else:
            messagebox.showinfo(title="Text Empty", message="There is nothing to convert!")

    def clear_text(self):
        """
        Clears any user-entered text from the Text-widget.
        """

        self.entered_text.delete("1.0", "end")

    def get_tld_code(self):
        """
        Sets the tld and code attributes for the language/accent selected in Option-Menu widget by looking up the
        selected language key in languages.json.
        """

        new_lang = self.option_var.get()
        self.TLD = self.lang_details[new_lang]["tld"]
        self.CODE = self.lang_details[new_lang]["code"]
