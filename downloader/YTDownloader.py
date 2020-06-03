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
from tkinter import ttk
from pytube import YouTube


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
        self.link_label = Label(self.master, text="Please enter the link here:",
                                fg="black", font=("Sans Serif", 20))
        self.link_label.grid(row=1)

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

        self.title_label = Label(self.master, fg="black", font=("Sans Serif", 20))

        self.confirmation_label = Label(self.master, fg="black", font=("Sans Serif", 20))

        self.confirmation_frame = Frame(self.master)

        self.yes_button = Button()
        self.no_button = Button()
        self.link = None
        self.choosing_dir_button = Button()
        self.directory_label = Label()
        self.proceed_button = Button()
        self.res_choices = ttk.Combobox()

    def check_link(self):
        self.link = self.youtubeEntry.get()
        # If an error occurs
        try:
            title = pytube.YouTube(self.link).title
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
                                 text="Yes", font=("Arial", 10), command=self.confirm_video)
        self.yes_button.pack(side=LEFT, padx=10)

        # Make sure that the no button is not yet on the screen
        self.no_button.pack_forget()
        # Not the video to download
        self.no_button = Button(self.confirmation_frame, width=5, bg="red", fg="white",
                                text="No", font=("Arial", 10), command=self.reject_video)
        self.no_button.pack(side=RIGHT)

        self.confirmation_frame.grid(row=6)

    def confirm_video(self):
        self.reject_video()
        self.link_label.grid_forget()
        self.entry.grid_forget()
        self.check_button.grid_forget()

        self.choosing_dir_button = Button(self.master, width=20, bg="green", fg="black",
                                          text="Choose Directory", font=("Arial", 20),
                                          command=self.choose_directory)
        self.choosing_dir_button.grid(row=2)

        self.directory_label = Label(self.master, font=("Helvetica", 15))
        self.directory_label.grid(row=3)

    def choose_directory(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 1:
            self.directory_label.config(text=folder_name)
            self.to_choose_res()
        else:
            self.directory_label.config(text="Please choose a folder!", fg="red")

    def to_choose_res(self):
        self.proceed_button = Button(self.master, width=10, bg="green", fg="black",
                                     text="Proceed", font=("Arial", 10), command=self.choose_res)
        self.proceed_button.grid(row=4)

    def choose_res(self):
        self.choosing_dir_button.grid_forget()
        self.directory_label.grid_forget()
        self.proceed_button.grid_forget()

        video = YouTube(self.link)

        res_dict = dict()
        for stream in video.streams.filter(progressive=True):
            res_dict[stream.itag] = stream.resolution
        res_values_list = list(res_dict.values())

        res_label = Label(self.master, fg="green", text="Please choose a resolution",
                          font=("Sans Serif", 20))
        res_label.grid(row=2)
        self.res_choices = ttk.Combobox(self.master, values=res_values_list)
        self.res_choices.grid(row=3)

        download_button = Button(self.master, width=10, bg="green", fg="black",
                                 text="Download", font=("Arial", 10),
                                 command=self.download)
        download_button.grid(row=4)

    def download(self):
        choice = self.res_choices.get()
        if choice is "":
            download_label = Label(self.master, fg="green", text="Choose a resolution",
                                   font=("Sans Serif", 20))
            download_label.grid(row = 5)
        else:
            download_label = Label(self.master, fg="green", text= choice + " video is downloading",
                                   font=("Sans Serif", 20))
            download_label.grid(row=5)

    def reject_video(self):
        # Delete the content in the field where the link will be pasted
        self.entry.delete(0, 'end')

        # Delete the shown title, the confirmation label, and the two buttons
        self.title_label.grid_forget()
        self.confirmation_label.grid_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()


root = Tk()
root.grid_columnconfigure(0, weight=1)
downloader_GUI = Window(root)
root.mainloop()
