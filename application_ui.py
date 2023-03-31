"""
CSC111 Winter 2023 Project:
MelodyMatch: Tailored Music Recommendations Derived From Your Spotify Habits

This Python module contains ...

Contributors: Manaljav Munkhbayar, Kevin Hu, Stanley Pang, Jaeyong Lee.
"""

import main
# import user_data
from math import ceil, floor
from tkinter import *
from PIL import ImageTk, Image

root = Tk()

# Sets Window Size and Position
# Width and Height depend on screen size
w_ratio = 5 / 6
h_ratio = 7 / 11
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
window_width, window_height = floor(screen_width * w_ratio), floor(screen_height * h_ratio)
x = ceil((screen_width/2) - (window_width/2))
y = ceil((screen_height/2) - (window_height/1.85))
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Window Titlebar: Name and Symbol
root.title('MelodyMatch')
logo = PhotoImage(file='gui/symbol.png')
root.iconphoto(False, logo)

# Background Colour
root['bg'] = '#0b2437'

# Logo
full_logo = ImageTk.PhotoImage(Image.open('gui/logo.png'))
full_logo_label = Label(root, image=full_logo, borderwidth=0)
full_logo_label.pack(pady=window_height * 0.05)

# Description
desc = Label(root,
             text='Welcome to MelodyMatch! \n\n'
                  "MelodyMatch is a personalized music recommendation app that analyzes your spotify \nlistening "
                  "history to suggest new songs that match your individual taste. By connecting \nyour Spotify "
                  "account, MelodyMatch will access your listening history. MelodyMatch then \nanalyzes your data to "
                  "suggest new songs that are tailored to your taste. \n MelodyMatch provides"
                  "an intuitive user experience, with a clean interface that is \neasy to navigate. Whether you're "
                  "looking to add new tracks to your favorite playlist or \nwant to explore new genres, MelodyMatch is "
                  "the perfect tool for discovering your next \nfavorite song.\n",
             bg='#0b2437',
             fg='White',
             font=('Verdana', 18))
desc.pack()


def create_label():
    new_label = Label(root, text="Stop server", bg='#0b2437', fg='White', font=('Verdana', 18))
    new_label.pack()


# Button
def start_button_event() -> None:
    """The event that happens when the following button is pressed"""
    main.run()

def end_button_event() -> None:
    """The event that happens when the following button is pressed"""
    # user_data.stop_server()
    print("i'm trying to kill the server!")


button = Button(root, text='Start', font=('Verdana', 12), command=(start_button_event))
button.pack()
button.config(width=10, height=2)

stop_button = Button(root, text='Stop', font=('Verdana', 12), command=(end_button_event))
stop_button.pack()
stop_button.config(width=10, height=2)
stop_button.place(x=50, y=50)

root.mainloop()
