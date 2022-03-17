<div align="center">

# Contest Bot
 
![badge](https://badgen.net/badge/version/v1.2.0/orange?style=flat-square)
![badge](https://badgen.net/badge/platform/win-32%20|%20win-64/green?style=flat-square)
![badge](https://badgen.net/badge/python/3/blue?style=flat-square)

A Reddit bot designed to randomly select the winners of a competition from top level comments in a post

  
<p align = "center">
  <img width="450" src="https://user-images.githubusercontent.com/44975876/157498158-16fbc847-945f-4a0b-9a29-aeb7a121c7b3.png">
</p>

  
[Getting started](#getting-started) •
[Project Files Description](#project-files-description) •
[Install Instructions](#install-instructions)
  
</div>

## Getting Started
To randomly select winners from a particular post, you:
  1. enter the amount of winners you want (defaults to 1)
  2. copy the URL of the post you are running the contest from
  3. click **Paste URL**, which will pull the post URL from the clipboard, and randomly select winners
 
 The selected winners will then be displayed in the text box. It shows up to a maximum of 10 before scrolling is required.

## Project Files Description

- :file_folder: **Excel Contest Records:** A directory containing contest results in a csv format
  - :page_facing_up: **Contest_??????.csv:** The contest results for the post with ID ??????
- :file_folder: **Logs:** contains up to 2 MB of program logs. This is used for debugging when an issue occurs
- :page_facing_up:  **account.ini:** Contains the user account information, which is required to access the Reddit API, and a user configurable list of blacklisted usernames
- :page_facing_up:  **contest_bot.pyw:** The main script the user should run

## Install Instructions
This script was developed and tested on Windows, but likely works on other operating systems. The python version installed was python 3.10.0. Installation for newer version of python 3 should look similar.

**1. Install Python 3**

  - Download and install the latest version of Python3 from [Python Downloads Page](https://www.python.org/downloads/), making sure to follow the below instructions during installation.
     - In the optional features menu, select **"pip"**, **"tcl/tk"**, **"py launcher"**, and **"for all users"**.
     - In the advanced  options menu: select **"Create shortcuts"**, **"Add Python to environment variables"**, and **"Precompile standard library"**
   
     <p align = "center">
       <img width="70%" alt="image" src="https://user-images.githubusercontent.com/44975876/157488978-aa671158-1161-4202-9f90-55f1f25e1698.png">
     </p>
     
   - Check that Python 3 is properly installed
     - First open a command prompt (cmd.exe), then run `python`. If it doesn't produce an error and looks similar to the example, then Python 3 is installed. Type `quit()` to exit Python 3
     - In the same command prompt, run `pip -V` (capital V), or `python -m pip -V`.  If it doesn't produce an error and looks similar to the example, then Pip is installed

     <p align = "center">
       <img width="70%" alt="image" src="https://user-images.githubusercontent.com/44975876/157490924-d4f9e061-73d1-48bf-b928-3e22a103edd6.png">
     </p>
     
**2. Install PRAW**
  
  - Open a command prompt, then run `pip install praw`, or `python -m pip install praw`
     - You should see an lot of output with the final line looking something like `Successfully installed praw-7.5.0 prawcore-2.3.0 update-checker-0.18.0`

**3. Install the script**

  - Create a folder where you'd like the script to live
  - Download the script files from github by clicking **Code** and then **Download Zip** as shown below
  - Unzip the files in `Contest-Bot-main.zip` into the folder you created

  <p align = "center">
    <img width="70%" alt="image" src="https://user-images.githubusercontent.com/44975876/157502508-4305fbbd-9bf2-4a20-a8ee-917c51ef40d5.png">
  </p>

**4. Complete account.ini**

  - Follow [the instructions in the praw documentation](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow) to get a `client_id` and `client_secret`. The `username` and `password` fields are just your normal Reddit account
