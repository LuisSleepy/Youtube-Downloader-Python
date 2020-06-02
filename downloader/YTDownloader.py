"""
Resources:
1. https://pythonbasics.org/tkinter-image/
2. https://github.com/nficano/pytube/issues/361
3. https://medium.com/quick-code/understanding-self-in-python-a3704319e5f0
4. https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
5. https://stackoverflow.com/questions/2260235/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter

"""

import pytube
from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import re
import tkinter as tk

class Window:
    entry_error = Label

    def __init__(self, master=None):
        self.title = None

        self.master = master
        master.title("YouTube Video Downloader")
        # For the main label
        main_label = Label(self.master, text="YouTube Video Downloader",
                           fg="blue", font=("Brandon Grotesque", 30))
        main_label.grid()

        # For the label on the Entry for the YouTube link
        link_label = Label(self.master, text="Please enter the link here:",
                           fg="black", font=("Sans Serif", 20))
        link_label.grid(row=1)

        # For getting the link
        entry_var = StringVar()
        self.entry = Entry(self.master, width=50, textvariable=entry_var)
        self.entry.grid(pady=(0, 10))

        self.youtubeEntry = Entry(self.master, width=50,
                                  textvariable=entry_var)

        # For checking the video
        self.check_button = Button(self.master, width=5, bg="blue", fg="white",
                                   text="Check", font=("Arial", 10), command=self.check_link)
        self.check_button.grid(row=3)

        self.entry_error = Label(self.master, text="", fg="red", font=("Helvetica", 15))
        self.entry_error.grid(pady=(0, 30))

        self.title_label = Label(self.master, fg = "black", font = ("Sans Serif", 20))

        self.confirmation_label = Label(self.master, fg="black", font=("Sans Serif", 20))

        self.confirmation_frame = Frame(self.master)

        self.yes_button = Button()
        self.no_button = Button()

    def check_link(self):
        entry = self.youtubeEntry.get()
        # If an error occurs
        try:
            print(entry)
            title = pytube.YouTube(entry).title
            self.show_title(title)
            self.entry_error['text'] = ""
        except pytube.exceptions.RegexMatchError:
            self.entry_error['text'] = "Invalid link"

    def show_title(self, title):
        self.title = title
        if self.title == "YouTube":
            self.entry_error['text'] = "Please try again"
            return

        self.title_label['text'] = self.title

        self.confirmation_label['text'] = "Is this the video you want to download?"

        self.title_label.grid(row=4)

        self.confirmation_label.grid(row=5)

        # Make sure first that the yes button is not yet on the screen
        self.yes_button.pack_forget()
        
        # Verifying the video to download
        self.yes_button = Button(self.confirmation_frame, width=5, bg="green", fg="white",
                            text="Yes", font=("Arial", 10))
        self.yes_button.pack(side=LEFT, padx=10)

        # Make sure that the no button is not yet on the screen
        self.no_button.pack_forget()
        # Not the video to download
        self.no_button = Button(self.confirmation_frame, width=5, bg="red", fg="white",
                           text="No", font=("Arial", 10), command=self.reject_video)
        self.no_button.pack(side=RIGHT)

        self.confirmation_frame.grid(row=6)

    def reject_video(self):
        # Delete the content in the field where the link will be pasted
        self.entry.delete(0, 'end')
        
        # Delete the shown title, the confirmation label, and the two buttons
        self.title_label.grid_forget()
        self.confirmation_label.grid_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()

    def download_video(self):
        link = pytube.YouTube(self.youtubeEntry.get())


root = Tk()
root.grid_columnconfigure(0, weight=1)
downloader_GUI = Window(root)
root.mainloop()
