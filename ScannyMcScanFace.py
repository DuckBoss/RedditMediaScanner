import praw
import wget
import urllib.request
import json
import os
import re
import datetime as dt
from time import sleep
import sys

class ScannyMcScanFace:

    reddit = praw.Reddit("bot1")
    subreddit_name = ""

    file_ext = [".jpg", ".png", ".gif"]
    url_type = ["gfycat", "imgur", "redd.it"]
    file_seek = []

    output_directory = "./DefaultDirectory/"
    sub = ""

    def __init__(self):
        print("ScannyMcScanFace Initialized!")
        print(dt.datetime.now())
        print("Current user: %s" % self.reddit.user.me())
        self.subreddit_name = sys.argv[1]
        self.output_directory = "./%s/" % self.subreddit_name
        print("Subreddit - %s" % self.subreddit_name)
        self.setupKeywords()
        self.sub = self.reddit.subreddit(self.subreddit_name)
        self.submissions = list(self.sub.new(limit=1024))
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def setupKeywords(self):
        if len(sys.argv) == 2:
            self.file_seek = [""]
            print("No Specific Keywords Given... Capturing All")
        elif len(sys.argv) > 2:
            for x in range(2, len(sys.argv)):
                self.file_seek.append(sys.argv[x].upper())
                print("Keyword Added - %s" % self.file_seek[x-2])

    def gfyFormat(self, submissionUrl):
        subSplit = submissionUrl.rsplit('/', 1)[1].rsplit('-', 1)[0].rsplit('.gif', 1)[0]
        jsonURL = "http://gfycat.com/cajax/get/%s" % subSplit
        with urllib.request.urlopen(jsonURL) as url:
            gfyData = json.loads(url.read().decode('utf-8'))
            gifURL = gfyData.get('gfyItem').get('gifUrl')
            submissionUrl = gifURL
        submissionUrl = gifURL
        return submissionUrl

    def fileNameFormat(self, fileName):
        fileName = re.sub('[^A-Za-z0-9]+', '', fileName)
        return fileName

    def historicalScan(self):
        print("Historical Submissions Capture Active...")
        for submission in self.submissions:
            if any(x in str.upper(submission.title) for x in self.file_seek):
                if submission.over_18:
                    continue
                submission_url = submission.url
                if any(y in submission_url for y in self.url_type):
                    if "gfycat" in submission_url:
                        if "albums" in submission_url:
                            continue
                        submission_url = self.gfyFormat(submission_url)

                    if any(z in submission_url for z in self.file_ext):
                        print(submission_url)
                        file_name = self.fileNameFormat(submission.title)
                        file_dir = ("%s%s.%s" % (self.output_directory, file_name, submission_url.rsplit('.',1)[1]))
                        print(file_dir)
                        if os.path.isfile(file_dir):
                            print("Already Exists - %s" %file_dir)
                            print("Skipping...")
                            continue
                        else:
                            wget.download(submission_url, out=file_dir)
                            print("\nFile Size: %s KB" % (os.path.getsize(file_dir)/1024))
        print("Historical Pictures Saved!")

    def realtimeScan(self):
        print("Real time Submissions Capture Active...")
        for submission in self.sub.stream.submissions():
            if any(x in str.upper(submission.title) for x in self.file_seek):
                if submission.over_18:
                    continue
                submission_url = submission.url
                if any(y in submission_url for y in self.url_type):
                    if "gfycat" in submission_url:
                        submission_url = self.gfyFormat(submission_url)

                    if any(z in submission_url for z in self.file_ext):
                        print(submission_url)
                        file_name = self.fileNameFormat(submission.title)
                        file_dir = ("%s%s.%s" % (self.output_directory, file_name, submission_url.rsplit('.',1)[1]))
                        if os.path.isfile(file_dir):
                            print("Already Exists - %s" %file_dir)
                            print("Skipping...")
                            continue
                        else:
                            print("Downloaded to - %s" %file_dir)
                            wget.download(submission_url, out=self.file_dir)
                            print("\nFile Size: %s KB" % (os.path.getsize(file_dir)/1024))
                        print("Waiting for new file...")
                        print("_______________________")
                        sleep(2)

def main():
    if len(sys.argv) < 2:
        print("ERROR: \nThis program requires atleast a subreddit to be specified.")
        print("You can leave the keywords argument blank to capture all content.")
        print("Format: python ScannyMcScanFace.py <subreddit_name> <keyword_1> <keyword_2> ...")
        sys.exit(1)

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
