import requests
import settings

reddit_client_id = settings.reddit_client_id
reddit_key = settings.reddit_key
reddit_application_name = settings.reddit_application_name


# req = requests.get("https://www.reddit.com/r/Xiaomi/new.json?sort=new", headers=headers)

def request_token():
    client_auth = requests.auth.HTTPBasicAuth(reddit_client_id, reddit_key)
    post_data = {"grant_type": "password", "username": "redditaleks", "password": "dag4v552"}
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                             headers=headers)
    print(response.json())
    access_token = response.json()["access_token"]
    return access_token


def get_my_info(access_token):
    headers = {"Authorization": "bearer {}".format(access_token),
               "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    print(response.json())

def get_subredit_by_string(access_token, search_string):
    headers = {"Authorization": "bearer {}".format(access_token),
               "User-Agent": "ChangeMeClient/0.1 by YourUsername"}

    params = {
        "exact":"",
        "include_over_18":"True",
        "include_unadvertisable":"True",
        "query": search_string
    }

    response = requests.post("https://oauth.reddit.com/api/search_subreddits", headers=headers, params=params)
    print(response.json())


if __name__ == '__main__':
    access_token = request_token()
    # get_my_info(access_token)
    get_subredit_by_string(access_token, "Xiaom")