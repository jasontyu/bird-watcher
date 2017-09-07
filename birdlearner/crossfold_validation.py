from __future__ import print_function

HAPPY_FILEPATH = "data/happy_sampled.txt"
SAD_FILEPATH = "data/sad_corpus.txt"
HAPPYSAD_FILEPATH = "data/happysad_equal_corpus.txt"
OUTPUT_FILEPATH = "data/cross_validate_output_with_terms_removed.txt"

def __main__():
    from classify import tokenize, selected_word_features
    from json import loads

    # Read in data
    happy, sad = read_happy_and_sad(HAPPY_FILEPATH, SAD_FILEPATH)

    # Select word features
    selected_words = select_features(HAPPYSAD_FILEPATH)

    # Apply cross validation
    cross_validate(selected_words, happy, sad)

def read_happy_and_sad(HAPPY_FILEPATH, SAD_FILEPATH):
    from classify import tokenize
    from json import loads
    print("READING IN DATA")
    all_happy_tokens, all_sad_tokens = [], []
    with open(HAPPY_FILEPATH, "r") as infile:
        all_happy_tokens = [ tokenize(loads(line)[u"text"]) for line in infile ]
    with open(SAD_FILEPATH, "r") as infile:
        all_sad_tokens = [ tokenize(loads(line)[u"text"]) for line in infile ]
    print(len(all_happy_tokens), len(all_sad_tokens))
    return all_happy_tokens, all_sad_tokens

def select_features(HAPPYSAD_FILEPATH):
    from classify import tokenize, selected_word_features
    from json import loads
    print("SELECTING WORD FEATURES")
    selected_words = []
    with open(HAPPYSAD_FILEPATH, "r") as infile:
        tokens = [ tokenize(loads(line)[u"text"]) for line in infile ]
        selected_words = selected_word_features(tokens)
    print(len(selected_words))
    return selected_words

def cross_validate(selected_words, happy, sad, n=5):
    from random import shuffle
    split_happy = int(len(happy) * 0.8)
    split_sad = int(len(sad) * 0.8)
    happy_correct = []
    sad_correct = []
    happy_total, sad_total = [], []
    for i in range(n):
        print("CROSS VALIDATION {}".format(i))

        shuffle(happy)
        shuffle(sad)
        h_train, h_test = happy[:split_happy], happy[split_happy:]
        s_train, s_test = sad[:split_sad], sad[split_sad:]
        partitioned_data = (h_train, s_train, h_test, s_test)

        results = simple_classification(partitioned_data, selected_words)

        hc, sc = results
        happy_correct.append(hc)
        sad_correct.append(sc)

        happy_total.append(len(h_test))
        sad_total.append(len(s_test))

        with open(OUTPUT_FILEPATH, "a") as outfile:
            outfile.write("\nClassification results {}\n".format(i))
            outfile.write("Number of predicted happy: {} (out of {})\n".format(
                happy_correct[i], happy_total[i]))
            outfile.write("Percent correct for happy: {}%\n".format(
                100*happy_correct[i] / happy_total[i]))
            outfile.write("Number of predicted sad: {} (out of {})\n".format(
                sad_correct[i], sad_total[i]))
            outfile.write("Percent correct for sad: {}%\n".format(
                100*sad_correct[i] / sad_total[i]))


    happy_percent = 100*sum(happy_correct) / sum(happy_total)
    sad_percent = 100*sum(sad_correct) / sum(sad_total)
    print(happy_percent, sad_percent)

    with open(OUTPUT_FILEPATH, "a") as outfile:
        outfile.write("\nAveraged classification results {}\n".format(i))
        outfile.write("Number of predicted happy: {} (out of {})\n".format(
            sum(happy_correct), sum(happy_total)))
        outfile.write("Percent correct for happy: {}%\n".format(
            100*sum(happy_correct) / sum(happy_total)))
        outfile.write("Number of predicted sad: {} (out of {})\n".format(
            sum(sad_correct), sum(sad_total)))
        outfile.write("Percent correct for sad: {}%\n".format(
            100*sum(sad_correct) / sum(sad_total)))
        outfile.write("Total correct: {} (out of {})\n".format(
            sum(happy_correct) + sum(sad_correct),
            sum(happy_total)+sum(sad_total)
        ))
        outfile.write("Percent correct for all: {}%\n".format(
            100*(sum(happy_correct)+sum(sad_correct))/(
                sum(happy_total)+sum(sad_total))
        ))

def features_set(corpus, selected_words):
    from classify import extracted_word_features
    return [ extracted_word_features(tokens, selected_words)
                            for tokens in corpus ]
def listify(fsets):
    from classify import ordered_list_of_dict
    return [ ordered_list_of_dict(fset) for fset in fsets ]


def simple_classification(partitioned_data, selected_words):
    from classify import extracted_word_features
    from classify import ordered_list_of_dict
    from json import loads
    from sklearn.naive_bayes import GaussianNB

    def features_set(corpus, selected_words):
        return [ extracted_word_features(tokens, selected_words)
                                for tokens in corpus ]
    def listify(fsets):
        return [ ordered_list_of_dict(fset) for fset in fsets ]

    # Unpack parameters
    happy_tokens,sad_tokens, happy_test,sad_test = partitioned_data

    # Extract word features from training set
    print("EXTRACTING WORD FEATURES")
    happy_features_set = features_set(happy_tokens, selected_words)
    sad_features_set = features_set(sad_tokens, selected_words)

    # Train on word features
    print("TRAINING ON WORD FEATURES")
    all_features_sets = happy_features_set + sad_features_set
    samples = listify(all_features_sets)
    labels = [ 1 for _ in happy_features_set ] + [ 0 for _ in sad_features_set ]
    model = GaussianNB()
    model.fit(samples, labels)

    # Test on word features
    print("TESTING")
    happy_test_samples = listify(features_set(happy_test, selected_words))
    sad_test_samples = listify(features_set(sad_test, selected_words))
    happy_predictions = model.predict(happy_test_samples)
    sad_predictions = model.predict(sad_test_samples)

    happy_correct = sum(happy_predictions)
    sad_correct = len(sad_predictions) - sum(sad_predictions)
    return (happy_correct, sad_correct)

if __name__ == "__main__":
    __main__()
