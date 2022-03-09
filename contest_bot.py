import praw
import string
import configparser

from random import choice
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkf
from tkinter import scrolledtext


class MainWindow(tk.Frame):
    def __init__(self, root, reddit):
        super().__init__(root)
        self.reddit = reddit
        self.root = root
        self.root.title("Contest Bot v1.2")
        self.root.columnconfigure(1, weight = 1)
        self.root.rowconfigure(0, weight = 1)
        self.root.rowconfigure(1, weight = 1)
        self.root.rowconfigure(2, weight = 999)
        self.grid()

        # Number of winners entry
        tk.Label(self.root, text = "Winners? : ").grid(row = 0, column = 0)
        self.entry_winners = ttk.Entry(self.root)
        self.entry_winners.grid(row = 0, column = 1, sticky = 'EW')
        self.entry_winners.insert(0, '1')

        # URL entry
        tk.Label(self.root, text = "URL: ").grid(row = 1, column = 0)
        self.entry_url = ttk.Entry(self.root)
        self.entry_url.grid(row = 1, column = 1, sticky = 'EW')

        # Winners list
        self.selected_winners = scrolledtext.ScrolledText(root)
        self.selected_winners.grid(row = 2, column = 0, columnspan=3, sticky = 'NESW')
        self.selected_winners.insert('1.0', "Enter, if you dare!!!")
        self.selected_winners.configure(state ='disabled')

        # Button to run program with URL in clipboard
        self.button_url = ttk.Button(self.root, text = 'Paste URL', command = self.run, width = 17)
        self.button_url.grid(row = 1, column = 2)

        # Set padding and minimal window size
        self.vertical_padding = 2
        self.horizontal_padding = 2
        for child in self.root.winfo_children():
            child.grid_configure(padx = self.horizontal_padding, pady = self.vertical_padding)
        self.root.update()
        minimum_window_size = self.calculate_window_size(2)
        self.root.minsize(*minimum_window_size)
        self.root.geometry("0x0")

    def calculate_window_size(self, text_box_lines):
        selected_winners_y_offset = self.selected_winners.winfo_rooty() - self.root.winfo_rooty() + self.vertical_padding + 4
        font_height = tkf.Font(font=self.selected_winners['font']).metrics('linespace')
        return (400, selected_winners_y_offset + text_box_lines * font_height)

    def get_winners(self, amount):

        # Verify records path exists
        records_path = Path.cwd() / 'Excel Contest Records'
        if not records_path.exists():
            records_path.mkdir(exist_ok = True)

        return [str(i+1) + ') account' + str(i) for i in range(amount)]

    def run(self):
        amount = self.entry_winners.get()
        if amount.isdigit():
            amount = int(amount)
            winners = self.get_winners(amount)

            self.selected_winners.configure(state ='normal')
            self.selected_winners.delete('1.0', tk.END)
            self.selected_winners.insert('1.0', "And the winners are:\n" + '\n'.join(winners))
            self.selected_winners.configure(state ='disabled')

            window_size = self.calculate_window_size(min(10, amount) + 1) # Show up to 10 winners at once
            self.root.geometry(f"0x{window_size[1]}")
        else:
            self.selected_winners.configure(state ='normal')
            self.selected_winners.delete('1.0', tk.END)
            self.selected_winners.insert('1.0', f"ERROR: \"{self.entry_winners.get()}\" is not a number...")
            self.selected_winners.configure(state ='disabled')

            self.root.geometry("0x0")


if __name__ == "__main__":
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

    root = tk.Tk()
    app = MainWindow(root, reddit)
    app.mainloop()
