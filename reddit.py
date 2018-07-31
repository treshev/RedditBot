import datetime
import json

import requests

import settings


class RedditAPI:
    reddit_client_id = settings.reddit_client_id
    reddit_key = settings.reddit_key
    reddit_application_name = settings.reddit_application_name
    token_start_time = None
    access_token = None

    def __init__(self):
        self.get_token()

    def get_token(self):
        if not self.access_token:
            token_start_time = datetime.datetime.now()
            self.access_token = self.request_token()
        elif (datetime.datetime.now() - self.token_start_time).seconds > 3590:
            # TODO: Надо переделать не рефреш
            self.access_token = self.request_token()

        return self.access_token

    def request_token(self):
        client_auth = requests.auth.HTTPBasicAuth(self.reddit_client_id, self.reddit_key)
        headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
        post_data = {"grant_type": "password", "username": "redditaleks", "password": "dag4v552"}

        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                                 headers=headers)
        access_token = response.json()["access_token"]
        print("access_token = ", access_token)
        return access_token

    def get_last_posts_from_subreddit(self, subbredit_name):
        responce = self.load_last_posts_from_reddit_by_subbredit_name(subbredit_name)
        post_list = self.parse_reddit_responce_to_posts_list(responce)

    def load_last_posts_from_reddit_by_subbredit_name(self, subreddit_name):
        headers = {'User-agent': 'your bot 0.1'}
        req = requests.get("https://www.reddit.com/r/{}/new.json?sort=new".format(subreddit_name), headers=headers)
        return req

    def parse_reddit_responce_to_posts_list(self, req):
        result = req.json()
        result_list = []
        for content in result['data']['children']:
            result_list.append({"title": content["data"]["title"],
                                "text": content["data"]["selftext"],
                                "url": content["data"]["url"],
                                "created": content["data"]["created"]})
        result_list.sort(key=lambda item: item["created"])
        return result_list


    def load_from_file(self):
        with open("test.txt", "r") as f:
            data = json.load(f)
        return data

    def search_subreddits(self, search_string):
        headers = {"Authorization": "bearer {}".format(self.access_token),
                   "User-Agent": "ChangeMeClient/0.1 by YourUsername"}

        params = {
            "exact": "",
            "include_over_18": "True",
            "include_unadvertisable": "True",
            "query": search_string
        }

        response = requests.post("https://oauth.reddit.com/api/search_subreddits", headers=headers, params=params)
        return(response.json()["subreddits"])


    def get_my_info(self, access_token):
        headers = {"Authorization": "bearer {}".format(access_token),
                   "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
        response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
        print(response.json())


if __name__ == '__main__':
    pass
