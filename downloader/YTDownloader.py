"""
A YouTube video downloader in Python programming language, using pytube

Author: janLuisAntoc
"""

import pytube
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pytube import YouTube
import socket


class Window:
    def __init__(self, master=None):
        self.master = master
        master.title("YouTube Video Downloader")
        # For the main label
        main_label = Label(self.master, text="YouTube Video Downloader",
                           fg="#FF0000", font=("Brandon Grotesque", 30))
        main_label.grid()

        # For the label on the Entry for the YouTube link
        self.link_label = Label(self.master, text="Please enter the link here:",
                                fg="#282828", font=("Sans Serif", 20))
        self.link_label.grid(row=1)

        # For getting the link
        entry_var = StringVar()
        self.entry = Entry(self.master, width=50, textvariable=entry_var)
        self.entry.grid(row=2)

        self.youtubeEntry = Entry(self.master, width=50,
                                  textvariable=entry_var)

        # A button for checking the video
        self.check_button = Button(self.master, width=5, bg="blue", fg="white",
                                   text="Check", font=("Arial", 10, "bold"), command=self.check_link)
        self.check_button.grid(row=3, pady=10)

        # Displays the possible error upon checking the video
        self.entry_error = Label(self.master, text="", fg="#FF0000", font=("Helvetica", 15))
        self.entry_error.grid(pady=(0, 30))

        # Label for displaying the title of the video
        self.title_label = Label(self.master, fg="#424141", font=("Helvetica", 20, "bold"))

        # Label for asking the confirmation from the user
        self.confirmation_label = Label(self.master, fg="black", font=("Sans Serif", 20))

        # Frame for the yes and no button for confirmation of the video
        self.confirmation_frame = Frame(self.master)
        # Frame for the restart and exit button in the last screen
        self.iter_frame = Frame(self.master)

        developer_label = Label(self.master, fg="#158BC6", font=("Sans Serif", 15, "italic"),
                                text="Developed by: SauceCute")
        developer_label.grid(row=7)

        # For the objects in the initial screen
        self.title = None
        self.yes_button = Button()
        self.no_button = Button()

        # For the objects in the second screen
        self.link = None
        self.to_init_screen_button = Button()
        self.choosing_dir_button = Button()
        self.directory_label = Label()
        self.proceed_button = Button()

        # For the objects in the third screen
        self.res_choices = ttk.Combobox()
        self.to_dir_screen_button = Button()
        self.res_label = Label()
        self.download_button = Button()
        self.download_label = Button()
        self.video = None
        self.restart_button = Button()
        self.exit_button = Button()

    # Controls the checking of the provided link for the video
    # Some errors not yet shown to the user:
    # 1. Empty or no link provided
    def check_link(self):
        # Make sure that the objects for confirming the video is not yet shown in the screen
        self.title_label.grid_forget()
        self.confirmation_frame.grid_forget()
        self.confirmation_label.grid_forget()

        self.link = self.youtubeEntry.get()
        try:
            socket.create_connection(("Google.com", 80))
            if self.link is "":
                self.entry_error['text'] = "Put the link above"
            else:
                title = pytube.YouTube(self.link).title
                if title == "YouTube":
                    self.entry_error['text'] = "An error occurred. Please try again."
                else:
                    self.show_title(title)
                    self.entry_error['text'] = ""
                    self.check_button['state'] = "disabled"
        # If an error occurs
        except OSError:
            self.entry_error['text'] = "No internet connection"
        except pytube.exceptions.RegexMatchError:
            self.entry_error['text'] = "Invalid link"

    # Controls the displaying of title
    def show_title(self, title):
        self.title = title

        # Not yet clear but this might be an error that occurred once
        if self.title == "YouTube":
            self.entry_error['text'] = "Please try again"
            return

        # Some characters are not readable (like emojis)
        # Fixed this problem by ignoring these special characters
        title_list = [self.title[j] for j in range(len(self.title)) if ord(self.title[j])
                      in range(65536)]
        title_str = ""
        for j in title_list:
            title_str = title_str + j

        self.title_label['text'] = title_str

        self.confirmation_label['text'] = "Is this the video you want to download?"

        self.title_label.grid(row=4)

        self.confirmation_label.grid(row=5)

        # Make sure first that the yes button is not yet on the screen
        self.yes_button.pack_forget()

        # Verifying the video to download
        self.yes_button = Button(self.confirmation_frame, width=5, bg="green", fg="white",
                                 text="Yes", font=("Arial", 10, "bold"), command=self.confirm_video)
        self.yes_button.pack(side=LEFT, padx=10)

        # Make sure that the no button is not yet on the screen
        self.no_button.pack_forget()
        # Not the video to download
        self.no_button = Button(self.confirmation_frame, width=5, bg="red", fg="white",
                                text="No", font=("Arial", 10, "bold"), command=self.reject_video)
        self.no_button.pack(side=RIGHT)

        self.confirmation_frame.grid(row=6)

    # Controls the program after confirming the video to download
    def confirm_video(self):
        # Removes any remnants of the initial screen
        self.reject_video()
        self.link_label.grid_forget()
        self.entry.grid_forget()
        self.check_button.grid_forget()

        # Button for choosing the directory
        self.choosing_dir_button = Button(self.master, width=20, bg="#2BAE66", fg="#FCF6F5",
                                          text="Choose Directory", font=("Arial", 20),
                                          command=self.choose_directory)
        self.choosing_dir_button.grid(row=2)

        # Label for the chosen directory
        self.directory_label = Label(self.master, font=("Helvetica", 15))
        self.directory_label.grid(row=3)

        # Button for going back to the initial screen
        self.to_init_screen_button = Button(self.master, width=10, bg="yellow", fg="black",
                                            text="Go Back", font=("Arial", 10, "bold"),
                                            command=self.restart_init_screen)
        self.to_init_screen_button.grid(row=5)

    # Goes back to the initial screen
    def restart_init_screen(self):
        # Remove everything seen on the directory screen
        self.choosing_dir_button.grid_forget()
        self.directory_label.grid_forget()
        self.to_init_screen_button.grid_forget()

        self.link_label.grid(row=1)
        self.entry.grid(row=2)
        self.check_button.grid(row=3, pady=10)
        self.proceed_button.grid_forget()

    # Clears mostly the objects in the second screen and applied to both confirming and rejecting
    # the video
    def reject_video(self):
        # Delete the content in the field where the link will be pasted
        self.entry.delete(0, 'end')

        # Delete the title, confirmation text, and the yes and no buttons
        self.title_label.grid_forget()
        self.confirmation_label.grid_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()

        self.check_button['state'] = "normal"

    # Controller for choosing the directory
    def choose_directory(self):
        # Allows opening the file dialog
        folder_name = filedialog.askdirectory()

        if len(folder_name) > 1:
            self.directory_label.config(text=folder_name)
            # Fixes the error of "Proceed" button appearing again in the main menu
            self.proceed_button.grid_forget()
            self.to_choose_res()
        else:
            self.directory_label.config(text="Please choose a folder!", fg="#FF0000")

    # Provides the proceed button going to the download screen
    def to_choose_res(self):
        self.proceed_button = Button(self.master, width=10, bg="#4AEE12", fg="black",
                                     text="Proceed", font=("Arial", 10, "bold"),
                                     command=self.choose_res)
        self.proceed_button.grid(row=4)

    # Goes back to the directory screen
    def restart_dir_screen(self):
        # Removes the content not seen on the directory screen
        self.res_label.grid_forget()
        self.res_choices.grid_forget()
        self.download_button.grid_forget()
        self.to_dir_screen_button.grid_forget()
        self.download_label.grid_forget()

        self.directory_label['text'] = ""
        self.choosing_dir_button.grid(row = 2)
        self.directory_label.grid(row = 3)
        self.to_init_screen_button.grid(row = 5)

    # Displays the objects on the download screen
    def choose_res(self):
        self.choosing_dir_button.grid_forget()
        self.directory_label.grid_forget()
        self.proceed_button.grid_forget()
        self.to_init_screen_button.grid_forget()

        self.video = YouTube(self.link)

        # Gets the available video resolution and display these through a Combo Box
        res_dict = dict()
        for stream in self.video.streams.filter(progressive=True):
            res_dict[stream.itag] = stream.resolution
        res_values_list = list(res_dict.values())

        self.res_label = Label(self.master, fg="green", text="Please choose a resolution",
                               font=("Sans Serif", 20))
        self.res_label.grid(row=2)
        self.res_choices = ttk.Combobox(self.master, values=res_values_list, state="readonly")
        self.res_choices.grid(row=3)

        self.download_button = Button(self.master, width=10, bg="#4AEE12", fg="black",
                                      text="Download", font=("Arial", 10, "bold"),
                                      command=self.download)
        self.download_button.grid(row=4)

        self.download_label = Label(self.master, fg="green", font=("Sans Serif", 15))
        self.download_label.grid(row=5)

        self.to_dir_screen_button = Button(self.master, width=10, bg="yellow", fg="black",
                                           text="Go Back", font=("Arial", 10, "bold"),
                                           command=self.restart_dir_screen)
        self.to_dir_screen_button.grid(row=6, pady=15)

    # Conducts the downloading of the video
    def download(self):
        choice = self.res_choices.get()
        if choice is "":
            self.download_label['text'] = "No resolution selected!"
        else:
            chosen_res = self.video.streams.get_by_resolution(choice)
            chosen_res.download(self.directory_label['text'])
            self.download_label['text'] = "Finished download. Download another video?"

            self.to_dir_screen_button.grid_forget()
            self.restart_button = Button(self.iter_frame, width=5, bg="green", fg="white",
                                         text="Yes", font=("Arial", 10, "bold"),
                                         command=self.restart)
            self.restart_button.pack(side=LEFT, padx=10)

            self.exit_button = Button(self.iter_frame, width=5, bg="red", fg="white",
                                      text="No", font=("Arial", 10, "bold"),
                                      command=self.master.destroy)
            self.exit_button.pack(side=RIGHT)

            self.iter_frame.grid(row=6)

    # Another run of the program
    def restart(self):
        self.master.destroy()
        start()

def start():
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    Window(root)
    root.mainloop()

start()
