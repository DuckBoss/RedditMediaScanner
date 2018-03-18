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

    file_ext = [".png", ".jpg", ".gif"]
    url_type = ["gfycat", "imgur", "redd.it"]
    file_seek = [""]

    output_directory = "./DefaultDirectory/"
    sub = ""

    # Custom Parameters
    allow_nsfw = False
    allow_stream = False
    search_limit = 1024

    def __init__(self):
        print("ScannyMcScanFace Initialized!")
        print(dt.datetime.now())
        print("Current user: %s" % self.reddit.user.me())
        self.subreddit_name = sys.argv[1]
        self.output_directory = "./%s/" % self.subreddit_name
        print("Subreddit - %s" % self.subreddit_name)
        self.setupKeywords()
        self.sub = self.reddit.subreddit(self.subreddit_name)
        self.submissions = list(self.sub.new(limit=self.search_limit))
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def setupKeywords(self):
        if len(sys.argv) == 2:
            self.file_seek = [""]
            print("Specific keywords/file extensions/parameters not provided... Capturing all media!")
        elif len(sys.argv) > 2:
            for x in range(2, len(sys.argv)):
                if sys.argv[x][0] is '-':
                    self.setupParams(sys.argv[x])
                    continue
                if sys.argv[x][0] is '[' and sys.argv[x][len(sys.argv[x])-1] is ']':
                    self.file_seek = list(map(str.upper, sys.argv[x].strip('[]').split(',')))
                    self.file_seek = [x.strip(' ') for x in self.file_seek]
                if sys.argv[x][0] is '(' and sys.argv[x][len(sys.argv[x])-1] is ')':
                    self.file_ext = list(map(str.lower, sys.argv[x].strip('()').split(',')))
                    self.file_ext = [x.strip(' ') for x in self.file_ext]
        
        for ext in self.file_ext:
            new_dir = ("%s%s" % (self.output_directory, ext))
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

        print ("Keywords - %s" % self.file_seek)
        print ("File Extensions - %s" % self.file_ext)
        print("\nPROCESSING INFORMATION...\n")

    def setupParams(self, parameter):
        #print("Custom parameter found: %s" % parameter[1:].strip())
        try:
            paramInt = int(parameter[1:])
            if paramInt >= 1 and paramInt <= 1024:
                self.search_limit = paramInt+1
                print("Paramater: search_limit = %s" % self.search_limit)
            else:
                self.search_limit = 1024
        except ValueError:
            self.search_limit = 1024

        if parameter[1:].strip() == 'nsfw':
            print("Parameter: allow_nsfw = True")
            self.allow_nsfw = True
        elif parameter[1:].strip() == 'stream':
            print("Parameter: allow_stream = True")
            self.allow_stream = True

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
        print("\nHistorical Submissions Capture Active...")
        print("_______________________")
        for submission in self.submissions:
            if any(x in str.upper(submission.title) for x in self.file_seek):
                if submission.over_18:
                    if self.allow_nsfw is False:
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
                        dir_check = "."+submission_url.rsplit('.',1)[1]
                        if dir_check in self.file_ext:
                            file_dir = ("%s%s/%s.%s" % (self.output_directory, dir_check, file_name, submission_url.rsplit('.',1)[1]))

                        if os.path.isfile(file_dir):
                            print("File Already Exists - %s" %file_dir)
                            print("Skipping...")
                            print("_______________________")
                            continue
                        else:
                            wget.download(submission_url, out=file_dir)
                            print("\nFile Size: %s KB" % (os.path.getsize(file_dir)/1024))
                            print("Waiting for new file...")
                            print("-----------------------")
        print("Historical Media Saved!")
        print("_______________________")

    def realtimeScan(self):
        print("\nReal Time Media Capture Active...")
        print("_______________________")
        for submission in self.sub.stream.submissions():
            if any(x in str.upper(submission.title) for x in self.file_seek):
                if submission.over_18:
                    if self.allow_nsfw is False:
                        continue
                submission_url = submission.url
                if any(y in submission_url for y in self.url_type):
                    if "gfycat" in submission_url:
                        submission_url = self.gfyFormat(submission_url)

                    if any(z in submission_url for z in self.file_ext):
                        print(submission_url)
                        file_name = self.fileNameFormat(submission.title)
                        file_dir = ("%s%s.%s" % (self.output_directory, file_name, submission_url.rsplit('.',1)[1]))
                        dir_check = "."+submission_url.rsplit('.',1)[1]
                        if dir_check in self.file_ext:
                            file_dir = ("%s%s/%s.%s" % (self.output_directory, dir_check, file_name, submission_url.rsplit('.',1)[1]))
                        
                        if os.path.isfile(file_dir):
                            print("Already Exists - %s" %file_dir)
                            print("Skipping...")
                            print("_______________________")
                            continue
                        else:
                            print("Downloaded to - %s" %file_dir)
                            wget.download(submission_url, out=file_dir)
                            print("\nFile Size: %s KB" % (os.path.getsize(file_dir)/1024))
                        print("Waiting for new file...")
                        print("-----------------------")
                        sleep(2)

def main():
    if len(sys.argv) < 2:
        print("-----------------------")
        print("ERROR: \nThis program requires atleast a subreddit to be specified.")
        print("You can leave the keywords argument blank to capture all content.")
        print("Format: python ScannyMcScanFace.py subreddit_name \"[keyword1, keyword2]\" \"(.png, .jpg, .gif)\" -optional_parameter ...")
        print("-----------------------")
        sys.exit(1)

    program = ScannyMcScanFace()
    startTime = dt.datetime.now()
    program.historicalScan()
    endTime = dt.datetime.now()
    print("Runtime: {}".format(endTime-startTime))
    print("\n\n")
    
    if(program.allow_stream):
        startTime = dt.datetime.now()
        program.realtimeScan()
        endTime = dt.datetime.now()
        print("Runtime: {}".format(endTime-startTime))

    sys.exit(0)

    


if __name__ == "__main__":
    main()
