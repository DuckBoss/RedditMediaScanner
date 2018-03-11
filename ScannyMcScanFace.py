import praw
import wget
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
    file_type = ["imgur", "redd.it"]
    
    #Chosen list of search keywords
    file_seek = ["PC"]
    
    #Chosen output directory.
    output_directory = "./Pics/"

    def __init__(self):
        print("ScannyMcScanFace Initialized!")
        print(dt.datetime.now())

    def scan(self):
        sub = self.reddit.subreddit(self.subreddit_name)
        
        # Creates output directory if it doesn't exist.
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        
        # Scans the last 1024 posts to get previously submitted data.
        print("Current user: %s" % self.reddit.user.me())
        self.submissions = list(sub.new(limit=1024))
        for submission in self.submissions:
            if any(x in str.upper(submission.title) for x in self.file_seek):
                submission_url = submission.url
                if any(y in submission_url for y in self.file_type):
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
        
        # Enables realtime submission data capture.
        for submission in sub.stream.submissions():
            if any(x in str.upper(submission.title) for x in self.file_seek):
                submission_url = submission.url
                if any(y in submission_url for y in self.file_type):
                    if any(z in submission_url for z in self.file_ext):
                        print(submission_url)
                        file_name = submission_url.rsplit('/', 1)[1]
                        file_dir = ("%s%s" % (self.output_directory, file_name))
                        if os.path.isfile(file_dir):
                            print("Already Exists - %s" %file_dir)
                            print("Skipping...")
                            
                            print("Waiting for new file...")
                            sleep(2)
                            continue
                        else:
                            print("Downloaded to - %s" %file_dir)
                            wget.download(submission_url, out=self.output_directory)
                            print("Waiting for new file...")
                            sleep(2)
                        
            


def main():
    startTime = dt.datetime.now()
    program = ScannyMcScanFace()
    program.scan()
    endTime = dt.datetime.now()
    print("Runtime: {}".format(endTime-startTime))



if __name__ == "__main__":
    main()
