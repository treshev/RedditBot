from reddit import RedditAPI




if __name__ == '__main__':
    # time.sleep(5)
    redditAPI = RedditAPI()
    redditAPI.load_posts_from_subreddit()


