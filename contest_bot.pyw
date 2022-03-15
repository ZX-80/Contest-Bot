import csv
import praw
import string
import random
import logging
import configparser
import tkinter as tk
import tkinter.font as tkf

from tkinter import ttk
from tkinter import scrolledtext
from pathlib import Path
from logging.handlers import RotatingFileHandler


class MainWindow(tk.Frame):
    def __init__(self, root, reddit, blacklist):
        super().__init__(root)
        self.root = root
        self.reddit = reddit
        self.blacklist = blacklist

        self.root.title("Contest Bot v1.2")
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=999)
        self.grid()

        # Number of winners entry
        tk.Label(self.root, text="Winners:").grid(row=0, column=0, sticky='W')
        self.entry_winners = ttk.Entry(self.root)
        self.entry_winners.grid(row=0, column=1, sticky="EW")
        self.entry_winners.insert(0, '1')

        # URL entry
        tk.Label(self.root, text="URL:").grid(row=1, column=0, sticky='W')
        self.entry_url = ttk.Entry(self.root)
        self.entry_url.grid(row=1, column=1, sticky="EW")
        self.entry_url.configure(state="readonly")

        # Winners list
        self.selected_winners = scrolledtext.ScrolledText(root)
        self.selected_winners.grid(row=2, column=0, columnspan=3, sticky="NESW")
        self.selected_winners.insert("1.0", "Winners will be listed here")
        self.selected_winners.configure(state="disabled")

        # Button to run program with URL in clipboard
        self.button_url = ttk.Button(self.root, text="Paste URL", command=self.run, width=17)
        self.button_url.grid(row=1, column=2)

        # Set padding and minimal window size
        self.vertical_padding = 2
        self.horizontal_padding = 2
        for child in self.root.winfo_children():
            child.grid_configure(padx=self.horizontal_padding, pady=self.vertical_padding)
        self.root.update()
        self.root.minsize(*self.calculate_window_size(3))
        self.root.geometry("0x0")

    def calculate_window_size(self, text_box_lines):
        selected_winners_y_offset = self.selected_winners.winfo_rooty() - self.root.winfo_rooty() + self.vertical_padding + 4
        font_height = tkf.Font(font=self.selected_winners["font"]).metrics("linespace")
        return (400, selected_winners_y_offset + text_box_lines * font_height)

    def set_selected_winners_text(self, text):
        self.selected_winners.configure(state="normal")
        self.selected_winners.delete("1.0", tk.END)
        self.selected_winners.insert("1.0", text)
        self.selected_winners.configure(state="disabled")
        self.selected_winners.update()

    def get_winners(self, post_URL, n):
        # Get all root comments from URL
        submission = reddit.submission(url=post_URL)
        submission.comments.replace_more(limit=None, threshold=1)
        root_comments = list(submission.comments)
        root_comments.sort(key=lambda comment: comment.created_utc) # Only take the latest root comment from an author
        root_comments = filter(lambda comment: comment.author not in self.blacklist, root_comments)
        deduplicated_comments = {comment.author : comment.body for comment in root_comments}

        # Select n winners
        winners = random.sample(list(deduplicated_comments.keys()), min(len(deduplicated_comments), n))
        winners.sort(key=lambda author: list(deduplicated_comments.keys()).index(author))

        # Store contest results in CSV file
        records_path = Path(__file__).parent.resolve() / "Excel Contest Records"
        records_path.mkdir(exist_ok=True)

        with open(records_path / f"Contest_{submission.id}.csv", 'w', newline='') as records_fp:
            writer = csv.writer(records_fp, escapechar = '\\', quoting=csv.QUOTE_NONE)
            writer.writerow(['Won?', '#', 'Name', 'Comment'])

            # NOTE: keys() is used instead of items(), as the order between them is not guaranteed to be the same
            for i, author in enumerate(deduplicated_comments.keys()):
                body = ''.join(list(filter(lambda x: x in string.printable and x not in "\t\n,", deduplicated_comments[author])))
                writer.writerow(['WINNER' if author in winners else '', str(i), author, body])

        return [str(list(deduplicated_comments.keys()).index(author)) + ") " + str(author) for i, author in enumerate(winners)]

    def run(self):
        # Get post URL from clipboard
        try:
            post_URL = root.selection_get(selection="CLIPBOARD")
        except tk.TclError as e:
            self.set_selected_winners_text(f"ERROR: {str(e)}\nNOTE: Probably no text in clipboard")
            self.root.geometry(f"0x0")
            raise
        
        self.entry_url.configure(state="normal")
        self.entry_url.delete(0, tk.END)
        self.entry_url.insert(0, post_URL)
        self.entry_url.configure(state="readonly")

        # Verify user entered a number
        amount = self.entry_winners.get()
        if amount.isdigit() and int(amount) == 0:
            self.set_selected_winners_text(f"ERROR: Winners must be more than 0")
            self.root.geometry("0x0")
        elif amount.isdigit():
            self.set_selected_winners_text("Processing...")

            try:
                winners = self.get_winners(post_URL, int(amount))
            except Exception as e:
                self.set_selected_winners_text(f"ERROR: {str(e)}")
                self.root.geometry(f"0x0")
                raise
             
            if len(winners) == 1:
                self.set_selected_winners_text(f"And the winner is:\n{winners[0]}")
            else:
                self.set_selected_winners_text(f"And the winners are:\n" + '\n'.join(winners))
            window_size = self.calculate_window_size(min(10, len(winners)) + 1) # Show up to 10 winners at once
            self.root.geometry(f"0x{window_size[1]}")
        else:
            self.set_selected_winners_text(f"ERROR: \"{amount}\" is not a number...")
            self.root.geometry("0x0")

if __name__ == "__main__":

    # Initialize logging
    logging.basicConfig(level=logging.NOTSET)
    logs_path = Path(__file__).parent.resolve() / "Logs"
    logs_path.mkdir(exist_ok=True)
    file_handler = RotatingFileHandler(logs_path / "contest_log.txt", maxBytes=1024*1024, backupCount=1) # 2 x 1M log files
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s"))
    logging.root.addHandler(file_handler)
    logger = logging.getLogger(__name__)
    logger.info("User started program.")

    try:
        # Initialize PRAW
        config = configparser.ConfigParser(allow_no_value=True)
        config.read("account.ini")
        reddit = praw.Reddit(
            client_id=config["ACCOUNT INFO"]["client id"],
            client_secret=config["ACCOUNT INFO"]["client secret"],
            password=config["ACCOUNT INFO"]["password"],
            user_agent="contest_bot/v1.2",
            username=config["ACCOUNT INFO"]["username"],
        )
        blacklist = list(config["BLACKLIST"])

        # Capture all Tk errors
        class FaultTolerantTk(tk.Tk):
            def report_callback_exception(self, exc, val, tb):
                logger.exception("Critical error occured in Tk.")

        # Initialize window
        root = FaultTolerantTk()
        app = MainWindow(root, reddit, blacklist)
        app.mainloop()
    except Exception as e:
        logger.exception("Critical error occured in main.")
        raise
