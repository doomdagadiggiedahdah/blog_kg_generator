# Walkthrough
- [![Walkthrough](https://img.youtube.com/vi/mUheCI9dYJc/0.jpg)](https://www.youtube.com/watch?v=mUheCI9dYJc)

## Installation
- `git clone` the repo
- install the requirements.txt (`pip install -r requirements.txt`)
- install cosma (instructions https://cosma.arthurperret.fr/installing.html)
- make a .creds file to store your FTP server info from the example.creds file (just run `cp example.creds .creds` to create the file, then add your info)
- the main call you need to make is to run the `update_cosma.sh` file (which also calls the `main.py` from within it). This is the single call you need to make.

## Program explanation and responsibilities
- To run this, run `blog_upload`.
- This will:
	- ask for the note that you want to upload
	- upload it
	- (start the graph generation, which will)
	- summarize your post
	- create graph
	- upload it to your website

