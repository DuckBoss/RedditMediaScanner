# RedditMediaScanner
This is a script that accesses a subreddit and downloads media content based on keywords from the submission title.

[![GitHub release](https://img.shields.io/badge/Build-1.2-brightgreen.svg)](https://github.com/DuckBoss/RedditMediaScanner-Python3/releases/latest)
[![Packagist](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/DuckBoss/RedditMediaScanner-Python3/blob/master/LICENSE)


## Dependencies
These dependencies, if you don't have them, can be installed with pip.
- praw
- wget
- configparser

## Usage
1) Setup a praw.ini file with your reddit username, password, user_agent, client_id, and client_secret.
> You can register the app with your account for authentication here: https://www.reddit.com/prefs/apps/
2) Keep the praw.ini file in the same directory as the python script.
3) Modify the config.ini file with your subreddit, search terms, optional parameters, etc...
> Refer to the config.ini section of the ReadMe for additional information.
4) Run the main.py script.

## config.ini file
```
subreddit_name -> name of the subreddit you wish to scan
search_terms -> list of keywords seperated by commas
output_directory -> an output directory address for downloaded media
file_extensions -> the types of files to download
url_types -> whitelisted websites/links to download from
search_limit -> the scan search limit (default=1024)
allow_nsfw -> allow/disallow scanning of nsfw content (default=False)
allow_stream -> allow/disallow continuous subreddit scanning for new media (default=False)
```
> If you mess something up, you can copy/paste the contents of the example_config.ini file into the config.ini file to reset it.

## praw.ini file
You can use the template provided in this repository and fill in the required information as detailed in the usage section of the readme.

## Bugs, Issues, or Feature Requests?
Use the github issue template provided in the repository.
