import configparser

class ConfigReader:
    search_terms = [""]
    search_subreddit = ""
    output_directory = ""
    file_extensions = [".jpg, .png, .gif"]
    url_types = [""]
    search_limit = 0
    allow_nsfw = False
    allow_stream = False

    def __init__(self):
        print("Config Reader Module Loaded!")

    def read_config(self):
        cp = configparser.ConfigParser()
        cp.read('config.ini')

        # Main Config
        self.search_terms = cp['Main']['search_terms'].replace(" ", "").split(',')
        self.search_subreddit = cp['Main']['search_subreddit'].split()[0]
        self.output_directory = cp['Main']['output_directory'].split()[0]

        # File Extensions/URL Types
        self.file_extensions = cp['File Extensions']['file_extensions'].replace(" ", "").split(',')
        self.url_types = cp['URL Types']['url_types'].replace(" ", "").split(',')

        # Optional
        self.search_limit = int(cp['Optional']['search_limit'])

        self.allow_nsfw = cp.getboolean('Optional', 'allow_nsfw')
        self.allow_stream = cp.getboolean('Optional', 'allow_stream')
