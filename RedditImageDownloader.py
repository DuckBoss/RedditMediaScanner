import praw
import wget
import os


def main():
    #requires a praw.ini file with the reddit user details and client details.
    reddit = praw.Reddit("bot1")
    
    #chosen subreddit...
    sub = reddit.subreddit("pcmasterrace")
    
    #file extension type to download...
    file_ext = [".jpg", ".png", ".gif"]
    
    #urls to search for...
    file_type = ["imgur", "redd.it"]
    
    #chosen keywords in a list...
    file_seek = ["PC"]
    
    #generated output directory...
    output_directory = "./Pics/"
    
    # Makes the output directory if it doesn't exist.
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(reddit.user.me())
    
    # Scans the last 1024 submissions.
    submissions = list(sub.new(limit=1024))
    for submission in submissions:
        if any(x in str.upper(submission.title) for x in file_seek):
            submission_url = submission.url
            if any(y in submission_url for y in file_type):
                if any(z in submission_url for z in file_ext):
                    print(submission_url)
                    file_name = submission_url.rsplit('/', 1)[1]
                    file_dir = ("%s%s" % (output_directory, file_name))
                    if os.path.isfile(file_dir):
                        continue
                    else:
                        wget.download(submission_url, out=output_directory)

    print("Historical Pictures Saved!")
    print("Real time Submissions Capture Active...")
    
    # Scans realtime submissions.
    for submission in sub.stream.submissions():
        if any(x in str.upper(submission.title) for x in file_seek):
            submission_url = submission.url
            if any(y in submission_url for y in file_type):
                if any(z in submission_url for z in file_ext):
                    print(submission_url)
                    file_name = submission_url.rsplit('/', 1)[1]
                    file_dir = ("%s%s" % (output_directory, file_name))
                    if os.path.isfile(file_dir):
                        print("Already Exists - %s" %file_dir)
                        print("Skipping...")
                        continue
                    else:
                        print("Downloaded to - %s" %file_dir)
                        wget.download(submission_url, out=output_directory)



if __name__ == "__main__":
    main()
