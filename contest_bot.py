import praw
import string
import configparser

from random import choice
from pathlib import Path
import tkinter as tk
from tkinter import ttk


# Initialize PRAW
config = configparser.ConfigParser()
config.read('account.ini')
reddit = praw.Reddit(
    client_id=config['ACCOUNT INFO']['client id'],
    client_secret=config['ACCOUNT INFO']['client secret'],
    password=config['ACCOUNT INFO']['password'],
    user_agent="contest_bot/v1.2",
    username = config['ACCOUNT INFO']['username'],
)

def get_winners():
    # Verify records path exists
    records_path = Path.cwd() / 'Excel Contest Records'
    if not records_path.exists():
        records_path.mkdir(exist_ok = True)
    # TODO (ZX-80): Complete function

# Initialize window
class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Contest Bot v1.2")
        self.root.geometry('400x50')
        #self.root.resizable(0,0)
        self.root.columnconfigure(1, weight = 1)
        self.root.rowconfigure(0, weight = 1)
        self.root.rowconfigure(1, weight = 1)
        self.root.rowconfigure(2, weight = 1000)
        self.grid()

        # URL entry
        tk.Label(self.root, text = "URL: ").grid(row = 0, column = 0)
        self.entry_url_text = tk.StringVar()
        self.entry_url = ttk.Entry(self.root, textvariable = self.entry_url_text)
        self.entry_url.grid(row = 0, column = 1, sticky = 'EW')

        self.button_url = ttk.Button(self.root, text = 'Paste URL', command = get_winners, width = 17)
        self.button_url.grid(row = 0, column = 2)

        # Number of winners entry
        tk.Label(self.root, text = "Winner #: ").grid(row = 1, column = 0)
        self.entry_winners_text = tk.StringVar()
        self.entry_winners = ttk.Entry(self.root, textvariable = self.entry_winners_text)
        self.entry_winners.grid(row = 1, column = 1, sticky = 'EW')
        self.entry_winners_text.set('1')


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.mainloop()

