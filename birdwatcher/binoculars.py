# Bird Watcher
# Twitter API authentication

import tweepy

def get_binoculars():
    from secrets import api_key, api_secret, access_token, access_secret

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    del api_key, api_secret, access_token, access_secret

    return api
