from reddit import RedditAPI




if __name__ == '__main__':
    # time.sleep(5)
    redditAPI = RedditAPI()
    list = redditAPI.get_last_posts_from_subreddit("gif")

    for item in list:
        print(item)



