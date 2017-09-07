def run_merge_files():
    from organize import merge_files, DATA_PATH
    emotional_files = [ DATA_PATH+"emotional_tweets_corpus2.txt",
                        DATA_PATH+"emotional_tweets_4.txt" ]
    merged_filepath = "data/happysad_corpus.txt"
    merge_files(emotional_files, merged_filepath)

def run_remove_repeated_tweets():
    from organize import remove_repeated_tweets
    in_filepath = "data/happysad_corpus_json.txt"
    out_filepath = "data/happysad_corpus_uniq.txt"
    remove_repeated_tweets(in_filepath, out_filepath)

def run_uncodify_file():
    from organize import uncodify_file
    in_filepath = "data/happysad_corpus.txt"
    out_filepath = "data/happysad_corpus_json.txt"
    uncodify_file(in_filepath, out_filepath)

def run_split_emotions():
    from organize import split_emotions
    happysad_filepath = "data/happysad_corpus_uniq.txt"
    happy_filepath = "data/happy_corpus.txt"
    sad_filepath = "data/sad_corpus.txt"
    split_emotions(happysad_filepath, happy_filepath, sad_filepath)


def run_sample_file():
    from organize import sample_file
    happy_filepath = "data/happy_corpus.txt"
    out_filepath = "data/happy_sampled.txt"
    numlines = 20000
    sample_file(happy_filepath, numlines, out_filepath)


def run_merge_files2():
    from organize import merge_files
    emotional_files = [ "data/happy_sampled.txt", "data/sad_corpus.txt" ]
    merged_filepath = "data/happysad_equal_corpus.txt"
    merge_files(emotional_files, merged_filepath)


def run_merge_files3():
    from organize import merge_files, DATA_PATH
    health_files = [ DATA_PATH + "test_healthcare.txt", DATA_PATH+"healthcare_tweets_2.txt"]
    merged_filepath = "data/healthcare.txt"
    merge_files(health_files, merged_filepath)
def run_uncodify_file_health():
    from organize import uncodify_file
    in_filepath = "data/healthcare.txt"
    out_filepath = "data/healthcare_json.txt"
    uncodify_file(in_filepath, out_filepath)
def run_remove_repeated_tweets_health():
    from organize import remove_repeated_tweets
    in_filepath = "data/healthcare_json.txt"
    out_filepath = "data/healthcare_uniq.txt"
    remove_repeated_tweets(in_filepath, out_filepath)

def prepare_soccer():
    from organize import DATA_PATH, uncodify_file, remove_repeated_tweets
    in_filepath = DATA_PATH + "soccer.txt"
    out_filepath = "data/soccer_json.txt"
    uncodify_file(in_filepath, out_filepath)
    from organize import remove_repeated_tweets
    in_filepath = out_filepath
    out_filepath = "data/soccer_uniq.txt"
    remove_repeated_tweets(in_filepath, out_filepath)

if __name__ == "__main__":


    # run_merge_files()
    #run_remove_repeated_tweets()
    #run_uncodify_file()
    #run_remove_repeated_tweets()
    #run_split_emotions()
    #run_sample_file()
    #run_merge_files2()

    #run_merge_files3()
    #run_uncodify_file_health()
    #run_remove_repeated_tweets_health()

    #prepare_soccer()
