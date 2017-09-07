from __future__ import print_function

DATA_PATH = "../birdwatcher/journal/"

def open_tweets(filepath):
    """
    Read a file containing JSON objects.

    Args:
        filepath (`str`): Local or full filepath of the file to be opened. File must
            be limited to only one JSON object per line. However, every line may not
            necessarily contain a JSON object.

    Returns:
        :obj: `list` of `dict`: List of JSON objects, parsed according to the 'loads'
            function in the 'json' module.

    """
    from json import loads
    from codecs import open

    with open(filepath, "r", "utf-8") as f:
        tweets = set( loads(line)["text"] for line in f if line )
        return list(tweets)

def merge_files(filepaths, merged_filepath):
    """Merges multiple documents into one"""
    from codecs import open
    with open(merged_filepath, "w", "utf-8") as outfile:
        for filepath in filepaths:
            with open(filepath, "r", "utf-8") as infile:
                for line in infile:
                    if line:
                        outfile.write(line)

def uncodify_file(in_filepath, out_filepath):
    """
    Converts JSON saved as {u'key':u'value} to {"key":"value"}.

    Fixes issue with reading a txt file containing JSON objects when stored
    without using json.dumps
    """
    from ast import literal_eval
    from json import dumps
    with open(in_filepath, "r") as infile:
        with open(out_filepath, "w") as outfile:
            for line in infile:
                outfile.write(dumps(literal_eval(line)))
                outfile.write("\n")

def remove_repeated_tweets(in_filepath, out_filepath):
    from json import loads
    from codecs import open
    seen = set()
    with open(in_filepath, "r", "utf-8") as infile:
        with open(out_filepath, "w", "utf-8") as outfile:
            for line in infile:
                tweet = loads(line)
                id_str = tweet[u"id_str"]
                if id_str not in seen: # if not duplicate
                    seen.add(id_str)
                    outfile.write(line)

def split_emotions(happysad_filepath, happy_filepath, sad_filepath):
    from json import loads, dumps
    from categories import happy, sad
    #import birdwatcher.categories
    #from categories import happy, sad

    # open infile
    # read JSON into memory
    tweets = []
    with open(happysad_filepath, "r") as infile:
        tweets = [ loads(line) for line in infile if line ]

    # for each tweet
    # check if happy or sad
    # save to correct file
    total_count = 0
    confused_count = 0
    with open(happy_filepath, "w") as happy_file:
        with open(sad_filepath, "w") as sad_file:
            for tweet in tweets:
                flag = 0
                text = tweet[u"text"]
                total_count += 1

                for happy_emoji in happy:
                    if happy_emoji in text:
                        flag += 1
                        break
                for sad_emoji in sad:
                    if sad_emoji in text:
                        flag -= 1
                        break

                if flag == 1:
                    happy_file.write(dumps(tweet))
                    happy_file.write("\n")
                elif flag == -1:
                    sad_file.write(dumps(tweet))
                    sad_file.write("\n")
                elif flag == 0:
                    confused_count += 1
                else:
                    print(tweet)
                    raise ValueError("flag unexpected value: {}".format(flag))
    print("Tweets removed for being too neutral: {}\nTotal lines processed: {}".format(confused_count, total_count))


def sample_file(in_filepath, numlines, out_filepath):
    from random import shuffle
    with open(in_filepath, "r") as infile:
        lines = infile.readlines()
        shuffle(lines)
        with open(out_filepath, "w") as outfile:
            for i,line in enumerate(lines):
                if i < numlines:
                    outfile.write(line)
