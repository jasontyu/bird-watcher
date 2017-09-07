# Bird Watcher
# Jason Yu
# April 14, 2017

from __future__ import print_function
import json
import tweepy
import datetime # used for time stamping program start/stop
import traceback

from util import unicodify

# Attributes I don't want
UNWANTED_ATTR = ["contributors", "current_user_retweet", "favorited", "geo",
    "id", "in_reply_to_status_id", "lang", "quoted_status_id", "retweeted",
    "source", "in_reply_to_user_id", "entities", "extended_entities",
    "in_reply_to_screen_name"]
UNWANTED_ATTR = unicodify(UNWANTED_ATTR)

# Nested attributes that I want
WANTED_NESTED_ATTR = { "user": ["followers_count", "friends_count",
                                "geo_enabled", "id_str", "location",
                                "protected", "time_zone", "statuses_count",
                                "created_at"],
                        "extended_tweet": ["full_text"]
}
WANTED_NESTED_ATTR = unicodify(WANTED_NESTED_ATTR)

def trim_tweet(tweet_json):
    """Trims and returns a tweet (JSON object).

    Deletes any irrelevant (eg perspectival) attributes, trims user information,
    and trims any nested quote tweets or retweets.

    TODO: Explain identifying information
    """
    # Trim unwated attributes
    for attr in tweet_json.keys():
        # Delete unwanted top-level attributes
        # Note: This approach saves any unexpected top-level attributes
        if attr in UNWANTED_ATTR:
            try:
                del tweet_json[attr]
            except KeyError:
                pass
        # Trim any expected nested attributes
        elif attr in WANTED_NESTED_ATTR:
            for sub_attr in tweet_json[attr].keys():
                if sub_attr not in WANTED_NESTED_ATTR[attr]:
                    del tweet_json[attr][sub_attr]

    # Trim nested tweets
    if u"quoted_status" in tweet_json.keys():
        tweet_json[u"quoted_status"] = trim_tweet(tweet_json[u"quoted_status"])
    if u"retweeted_status" in tweet_json.keys():
        tweet_json[u"retweeted_status"] = trim_tweet(tweet_json[u"retweeted_status"])

    return tweet_json

def log_start(desc=None):
    with open("journal/logs.txt", "a") as logf:
        logf.write("Program start: ")
        logf.write(str(datetime.datetime.now()))
        if desc is not None:
            logf.write(" || ")
            logf.write(desc)
        logf.write("\n")

def log_stop(desc=None):
    with open("journal/logs.txt", "a") as logf:
        logf.write("Program stop: ")
        logf.write(str(datetime.datetime.now()))
        if desc is not None:
            logf.write(" || ")
            logf.write(desc)
        logf.write("\n")

# Define stream behavior, inheriting from tweepy.StreamListener
# See: https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py
class MyStreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        """Called when raw data is received from connection."""
        data = json.loads(raw_data)

        if u"in_reply_to_status_id_str" in data:
            tweet = trim_tweet(data)
            with open("journal/emotional_tweets_4.txt", "a") as f:
                f.write(str(tweet))
                f.write("\n")
        elif u"limit" in data:
            pass
        else:
            with open("journal/unrecognized.txt", "a") as f:
                f.write(data)



def main():
    from binoculars import get_binoculars
    from categories import happysad
    import sys # to access arguments of program call

    api = get_binoculars()
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    if len(sys.argv) > 1:
        desc = " ".join(sys.argv[1:])
        log_start(desc)
    else:
        log_start()
    myStream.filter(languages=[u"en"], track=happysad)


if __name__ == "__main__":

    while True:
        try:
            main()
        except KeyboardInterrupt:
            log_stop("Keyboard Interrupt")
            break
        except Exception as e:
            log_stop(str(e))
            traceback.print_exc()
            print("Time of error: ")
            print(str(datetime.datetime.now()))
            print("\n")

            continue
