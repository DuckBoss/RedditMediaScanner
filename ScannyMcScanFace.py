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
        self.sub = self.reddit.subreddit(self.subreddit_name)
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def gfyFormat(self, submissionUrl):
        subSplit = submissionUrl.rsplit('/', 1)[1].rsplit('-', 1)[0].rsplit('.gif', 1)[0]
        jsonURL = "http://gfycat.com/cajax/get/%s" % subSplit
        with urllib.request.urlopen(jsonURL) as url:
            gfyData = json.loads(url.read().decode('utf-8'))
            gifURL = gfyData.get('gfyItem').get('gifUrl')
            submissionUrl = gifURL
        submissionUrl = gifURL
        return submissionUrl

    def historicalScan(self):
        print("Current user: %s" % self.reddit.user.me())
        self.submissions = list(self.sub.new(limit=1024))
        for submission in self.submissions:
            if any(x in str.upper(submission.title) for x in self.file_seek):
                submission_url = submission.url
                if any(y in submission_url for y in self.file_type):
                    if "gfycat" in submission_url:
                        submission_url = self.gfyFormat(submission_url)

                    if any(z in submission_url for z in self.file_ext):
                        print(submission_url)
                        file_name = submission_url.rsplit('/', 1)[1]
                        file_dir = ("%s%s" % (self.output_directory, file_name))
                        if os.path.isfile(file_dir):
                            continue
                        else:
                            wget.download(submission_url, out=self.output_directory)
        print("Historical Pictures Saved!")

    def realtimeScan(self):
        print("Real time Submissions Capture Active...")
        for submission in self.sub.stream.submissions():
            if any(x in str.upper(submission.title) for x in self.file_seek):
                submission_url = submission.url
                if any(y in submission_url for y in self.file_type):
                    if "gfycat" in submission_url:
                        submission_url = self.gfyFormat(submission_url)

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
    program = ScannyMcScanFace()
    startTime = dt.datetime.now()
    program.historicalScan()
    endTime = dt.datetime.now()
    print("Runtime: {}".format(endTime-startTime))
    print("\n\n")
    startTime = dt.datetime.now()
    program.realtimeScan()
    endTime = dt.datetime.now()
    print("Runtime: {}".format(endTime-startTime))


if __name__ == "__main__":
    main()
