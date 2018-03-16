# ScannyMcScanFace-Python3
This is a script that accesses a subreddit and downloads images based on keywords from the submission title.

## Dependencies
- praw (can be installed with pip)
- wget (can be installed with pip)


## Usage
1) Setup a praw.ini file with your reddit username, password, user_agent, client_id, and client_secret.
2) Keep the praw.ini file in the same directory as the python script.
3) Run the script with the following format that uses system arguments:
```
python ScannyMcScanFace.py <subreddit_name> <keyword_1> <keyword_2> ...
```
> You may choose to not include any keywords, which will capture all media available instead of submissions with keywords.

## praw.ini file
You can use the template provided in this repository and fill in the required information as detailed in the usage section of the readme.
