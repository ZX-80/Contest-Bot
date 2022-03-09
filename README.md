# Contest-Bot
A Reddit bot designed to select winners from top level comments in a post

<img width="33%" alt="image" src="https://user-images.githubusercontent.com/44975876/157498158-16fbc847-945f-4a0b-9a29-aeb7a121c7b3.png">

**Winners:** Here the user may enter how many winners they wish to select. (default is 1)

**URL:** This displays the URL of the post that the bot is selecting from.

**Paste URL:** Clicking this will pull the post URL from the clipboard, and randomly select winners.

**Text Box:** This is where the winners will be displayed. It shows up to a maximum of 10 before scrolling is required.

## How to use
Enter the amount of winners you want if it's more than one. Then, simply copy the URL of the post you are running the contest from, and click **Paste URL** in the program. A list of winners will then be displayed in the text box.

## Script Files/Directories

- :file_folder: **Excel Contest Records:** A directory containing contest results in a csv format
  - :page_facing_up: **Contest_??????.csv:** The contest results for the post with ID ??????
- :file_folder: **Logs:** contains up to 2 MB of program logs. This is used for debugging when an issue occurs
- :page_facing_up:  **account.ini:** Contains the user account information which is required to access the Reddit API
- :page_facing_up:  **contest_bot.pyw:** The main script the user should run

## Install Instructions
This script was developed and tested on Windows, but likely works on other operating systems. The python version installed was python 3.10.0. Installation for newer version of python 3 should look similar.

**1. Install Python 3**

  1. Download and install the latest version of Python3 from [Python Downloads Page](https://www.python.org/downloads/), making sure to follow the below instructions during installation.
     - In the optional features menu, select **"pip"**, **"tcl/tk"**, **"py launcher"**, and **"for all users"**.
     - In the advanced  options menu: select **"Create shortcuts"**, **"Add Python to environment variables"**, and **"Precompile standard library"**
   
     <p align = "center">
       <img width="70%" alt="image" src="https://user-images.githubusercontent.com/44975876/157488978-aa671158-1161-4202-9f90-55f1f25e1698.png">
     </p>
     
  2. Check that Python 3 is properly installed
     - First open a command prompt (cmd.exe), then run `python`. If it doesn't produce an error and looks similar to the example, then Python 3 is installed. Type `quit()` to exit Python 3
     - In the same command prompt, run `pip -V` (capital V), or `python -m pip -V`.  If it doesn't produce an error and looks similar to the example, then Pip is installed

     <p align = "center">
       <img width="70%" alt="image" src="https://user-images.githubusercontent.com/44975876/157490924-d4f9e061-73d1-48bf-b928-3e22a103edd6.png">
     </p>
     
**2. Install PRAW**
  
  1. Open a command prompt, then run `pip install praw`, or `python -m pip install praw`
     - You should see an lot of output with the final line looking something like `Successfully installed praw-7.5.0 prawcore-2.3.0 update-checker-0.18.0`

**3. Install the script**

  1. Create a folder where you'd like the script to live
  2. Download the script files from github by clicking **Code** and then **Download Zip** as shown below
  3. Unzip the files in `Contest-Bot-main.zip` into the folder you created

  <p align = "center">
    <img width="70%" alt="image" src="https://user-images.githubusercontent.com/44975876/157502508-4305fbbd-9bf2-4a20-a8ee-917c51ef40d5.png">
  </p>

**4. Complete account.ini**

  1. Follow [the instructions in the praw documentation](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow) to get a `client_id` and `client_secret`. The `username` and `password` fields are just your normal Reddit account
