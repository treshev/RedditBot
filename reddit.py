import json

import requests

import settings

reddit_client_id = settings.reddit_client_id
reddit_key = settings.reddit_key
reddit_application_name = settings.reddit_application_name


def get_last_messages():
    req = load_from_reddit_and_save_to_file()
    result = req.json()
    result_list = []
    for content in result['data']['children']:
        result_list.append({"title": content["data"]["title"],
                            "text": content["data"]["selftext"],
                            "url": content["data"]["url"],
                            "created": content["data"]["created"]})
    result_list.sort(key=lambda item: item["created"])
    return result_list


def load_from_reddit_and_save_to_file():
    headers = {'User-agent': 'your bot 0.1'}
    # req = requests.get("https://www.reddit.com/r/Xiaomi/new.json?sort=new", headers=headers)
    req = requests.get("https://www.reddit.com/r/FuckHerFace/new.json?sort=new", headers=headers)
    with open("test.txt", "w") as f:
        json.dump(req.json(), f)
    return req


def load_from_file():
    with open("test.txt", "r") as f:
        data = json.load(f)
    return data


def search_subreddits(find_string):
    headers = {'User-agent': 'your bot 0.1'}
    params = {
        "exact": "",
        "include_over_18": "",
        "include_unadvertisable": "",
        "query": "",
    }

    req = requests.get("https://www.reddit.com/r/Xiaomi/new.json?sort=new", headers=headers)
    return req
