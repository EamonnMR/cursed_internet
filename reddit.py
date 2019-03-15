import requests

VERSION = "0.0.1"

def stories_for_sub(subreddit, stories=10):
    headers = {
            "User-Agent": "unix:cursed-internet:v{} (by /u/EamonnMR)".format(VERSION)
    }
    response = requests.get(
            "http://reddit.com/r/{}/top/.json?count={}".format(subreddit, stories),
            headers=headers)

    response.raise_for_status()


    return [x['data']['title'] for x in response.json()['data']['children']]

