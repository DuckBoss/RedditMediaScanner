# ScannyMcScanFace-Python3
This is a script that accesses a subreddit and downloads images based on keywords from the submission title.

[![GitHub release](https://img.shields.io/badge/Build-1.1-brightgreen.svg)](https://github.com/DuckBoss/ScannyMcScanFace-Python3/releases/latest)
[![Packagist](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/DuckBoss/ScannyMcScanFace-Python3/blob/master/LICENSE)


## Dependencies
- praw (can be installed with pip)
- wget (can be installed with pip)

## Usage
1) Setup a praw.ini file with your reddit username, password, user_agent, client_id, and client_secret.
> You can register the app with your account for authentication here: https://www.reddit.com/prefs/apps/
2) Keep the praw.ini file in the same directory as the python script.
3) Run the script with the following format that uses system arguments:
```
python ScannyMcScanFace.py subreddit_name "[keyword_1, keyword_2]" "(file_extension_1, file_extension_2)" -optional_params
```

## Example Usage:
- Full run using keywords, file extensions, and optional parameters.
```
python ScannyMcScanFace.py all "[ducks, penguins]" "(.png, .jpg, .gif)" -stream
```
- Simple run using just the subreddit. This will capture all media with the default file extensions (png, jpg, gif).
```
python ScannyMcScanFace.py all
```
- Mixed run using just keywords, and no custom file extensions or parameters.
```
python ScannyMcScanFace.py all "[ducks, penguins]"
```
> You may choose to not include any keywords, which will capture all media available instead of submissions with keywords.
> You may choose to not include custom file extensions. This will cause the script to capture media with the default file extensions (png, gif, jpg).
> Optional parameters are not required to run the script. They are used to filter specific submissions.

## praw.ini file
You can use the template provided in this repository and fill in the required information as detailed in the usage section of the readme.

## All Optional Parameters
- stream (format: -stream) (enables real time capturing)
- allow_nsfw (format: -allow_nsfw) (allows nsfw media to be captured)
- search_limit (format: -any_integer, example: -400) (limits the number of submissions that are scanned)
