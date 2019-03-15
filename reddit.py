import requests

VERSION = "0.0.1"

def stories_for_sub(subreddit, stories=10):
    headers = {
            "User-Agent": "unix:cursed-internet:v{} (by /u/EamonnMR)".format(VERSION)
    }
    return requests.get(
            "http://reddit.com/r/{}/top/.json?count={}".format(subreddit, stories),
            headers=headers)

