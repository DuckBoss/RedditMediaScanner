import praw
import wget
import urllib.request
import json
import os
import datetime as dt
from time import sleep
import sys

class ScannyMcScanFace:

    reddit = praw.Reddit("bot1")
    
    #Chosen subreddit. Please be mindful of any blacklisted subreddits.
    subreddit_name = "pcmasterrace"
    #Allowed list of File Extensions
    file_ext = [".jpg", ".png", ".gif"]
    #Allowed list of URL Types
    file_type = ["gfycat", "imgur", "redd.it"]
    #Chosen list of search keywords. Please put all keywords in CAPITAL letters.
    file_seek = ["PC"]
    #The output directory is named after the chosen subreddit.
    output_directory = "./%s/" % subreddit_name

    def __init__(self):
        print("ScannyMcScanFace Initialized!")
        print(dt.datetime.now())

    def scan(self):
        sub = self.reddit.subreddit(self.subreddit_name)

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        print("Current user: %s" % self.reddit.user.me())
        self.submissions = list(sub.new(limit=1024))
        for submission in self.submissions:
            if any(x in str.upper(submission.title) for x in self.file_seek):
                if submission.over_18:
                    continue
                submission_url = submission.url
                if any(y in submission_url for y in self.file_type):
                    if "gfycat" in submission_url:
                            subSplit = submission_url.rsplit('/', 1)[1]
                            jsonURL = "http://gfycat.com/cajax/get/%s" % subSplit
                            with urllib.request.urlopen(jsonURL) as url:
                                gfyData = json.loads(url.read().decode())
                                gifURL = gfyData.get('gfyItem').get('gifUrl')
                                submission_url = gifURL

                    if any(z in submission_url for z in self.file_ext):
                        print(submission_url)
                        file_name = submission_url.rsplit('/', 1)[1]
                        file_dir = ("%s%s" % (self.output_directory, file_name))
                        if os.path.isfile(file_dir):
                            continue
                        else:
                            wget.download(submission_url, out=self.output_directory)

        print("Historical Pictures Saved!")
        print("Real time Submissions Capture Active...")

        for submission in sub.stream.submissions():
            if any(x in str.upper(submission.title) for x in self.file_seek):
                if submission.over_18:
                    continue
                submission_url = submission.url
                if any(y in submission_url for y in self.file_type):
                    if "gfycat" in submission_url:
                            subSplit = submission_url.rsplit('/', 1)[1]
                            jsonURL = "http://gfycat.com/cajax/get/%s" % subSplit
                            with urllib.request.urlopen(jsonURL) as url:
                                gfyData = json.loads(url.read().decode())
                                gifURL = gfyData.get('gfyItem').get('gifUrl')
                                submission_url = gifURL

                    if any(z in submission_url for z in self.file_ext):
                        print(submission_url)
                        file_name = submission_url.rsplit('/', 1)[1]
                        file_dir = ("%s%s" % (self.output_directory, file_name))
                        if os.path.isfile(file_dir):
                            print("Already Exists - %s" %file_dir)
                            print("Skipping...")
                        else:
                            print("Downloaded to - %s" %file_dir)
                            wget.download(submission_url, out=self.output_directory)
                        print("Waiting for new file...")
                        print("_______________________")
                        sleep(2)
                        
            


def main():
    startTime = dt.datetime.now()
    program = ScannyMcScanFace()
    program.scan()
    endTime = dt.datetime.now()
    print("Runtime: {}".format(endTime-startTime))



if __name__ == "__main__":
    main()
