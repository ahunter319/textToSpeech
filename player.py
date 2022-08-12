import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import shutil
import styles as st
from resources import resource_path


class MP3Player(tk.Frame):
    """
    MP3Player class is a tk.Frame used to load, play, pause, restart, and save an mp3 file.

    Methods:
        __init__(self, parent)
        load_music(self)
        play_pause(self)
        reset_player(self)
        save_mp3(self)
    """

    def __init__(self, parent):
        super().__init__()
        """MP3Player class constructor to initialize the object.

        Input Arguments: parent must be Tk() object
        """

        # Frame setup
        self["borderwidth"] = 2
        self["relief"] = "raised"
        self["background"] = st.GREY

        # Initial attributes
        self.welcome_path = resource_path("out/welcome.mp3")
        self.speech_path = resource_path("out/output.mp3")

        self.welcome_on = True
        self.is_playing = False
        self.has_started = False

        # Initializing mp3 player
        pygame.init()
        pygame.mixer.music.load(self.welcome_path)

        # Creating/Placing Button-widget with back/replay image, calls reset_player method
        self.back_img = tk.PhotoImage(file=resource_path("images/back.png"))
        self.back_resized = self.back_img.subsample(13, 13)
        self.reset_player_btn = tk.Button(self, image=self.back_resized, bg=st.GREY, borderwidth=0,
                                          command=self.reset_player)
        self.reset_player_btn.grid(column=0, row=0, padx=5, pady=5)

        # Loading/resizing play and pause images
        self.play_img = tk.PhotoImage(file=resource_path("images/play.png"))
        self.play_img_res = self.play_img.subsample(13, 13)
        self.pause_img = tk.PhotoImage(file=resource_path("images/pause.png"))
        self.pause_img_res = self.pause_img.subsample(13, 13)

        # Creating/Placing Button-widget with play/pause images, calls play_pause method
        self.play_pause_img = self.play_img_res
        self.play_pause_btn = tk.Button(self, image=self.play_pause_img, bg=st.GREY, borderwidth=0,
                                        command=self.player_wrapper)
        self.play_pause_btn.grid(column=1, row=0, padx=5, pady=5)

        # Creating/Placing Button-widget, calls save_mp3 method
        self.save_btn = tk.Button(self, text="Save to MP3", command=self.save_mp3)
        self.save_btn.grid(column=2, row=0, padx=5, pady=5)

    def load_music(self):
        """
        Loads mp3 in given speech_path to pygame's mixer. Callable from pdf and text converters.
        """
        pygame.mixer.music.load(self.speech_path)

    def play_pause(self, path):
        """
        Detects the playing-state of mp3 and plays/pauses it accordingly. Also updates the button image to display
        either play or pause symbol depending on if the mixer is playing or not.
        """

        if self.has_started:
            if self.is_playing:
                # Mp3 has been played
                pygame.mixer.music.pause()
                self.play_pause_btn.configure(image=self.play_img_res)
                self.is_playing = False
            else:
                # Mp3 has been played but is currently paused
                pygame.mixer.music.unpause()
                self.play_pause_btn.configure(image=self.pause_img_res)
                self.is_playing = True
        else:
            # Mp3 has not been played at all yet
            self.has_started = True
            self.is_playing = True
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.play_pause_btn.configure(image=self.pause_img_res)

    def player_wrapper(self):
        """
        Decides whether to play welcome message or speech depending on if first play-through.
        """
        if self.welcome_on:
            self.play_pause(self.welcome_path)
        else:
            self.play_pause(self.speech_path)

    def reset_player(self):
        """
        Resets the mp3 player/mixer back to the never-been-played state. Resets play/pause image to 'play' symbol.
        """

        pygame.mixer.music.unload()
        self.has_started = False
        self.play_pause_btn.configure(image=self.play_img_res)

    def save_mp3(self):
        """
        Saves the generated mp3 to user-selected file-path.
        """

        user_file_name = filedialog.asksaveasfilename(parent=self, title="Enter a Filename")
        new_path = f"{user_file_name}.mp3"

        if user_file_name:
            # Copying output mp3 to user's path
            destination = shutil.copy(self.speech_path, new_path)
            messagebox.showinfo(title="Success", message=f"Your file has been saved to {destination}")
        else:
            messagebox.showinfo(title="Error", message="You must provide a location and filename. Please try again.")


# play/pause/reset icons made by nawicon from www.flaticon.com