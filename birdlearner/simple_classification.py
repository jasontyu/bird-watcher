

HAPPY_FILEPATH = "data/happy_corpus.txt"
SAD_FILEPATH = "data/sad_corpus.txt"
HAPPYSAD_FILEPATH = "data/happysad_equal_corpus.txt"
OUTPUT_FILEPATH = "data/simple_test_output_with_terms_removed.txt"




def __main__():
    from classify import tokenize, selected_word_features, extracted_word_features
    from classify import partition_corpora, ordered_list_of_dict
    from json import loads
    from sklearn.naive_bayes import GaussianNB

    def features_set(corpus, selected_words):
        return [ extracted_word_features(tokens, selected_words)
                                for tokens in corpus ]
    def listify(fsets):
        return [ ordered_list_of_dict(fset) for fset in fsets ]


    # Read in data
    print("READING IN DATA")
    all_happy_tokens, all_sad_tokens = [], []
    with open(HAPPY_FILEPATH, "r") as infile:
        all_happy_tokens = [ tokenize(loads(line)[u"text"]) for line in infile ]
    with open(SAD_FILEPATH, "r") as infile:
        all_sad_tokens = [ tokenize(loads(line)[u"text"]) for line in infile ]
    corpora = (all_happy_tokens, all_sad_tokens)

    # Partition data into training/testing sets
    training, testing = partition_corpora(corpora)
    happy_tokens, sad_tokens = training
    happy_test, sad_test = testing
    print(len(happy_tokens), len(sad_tokens), len(happy_test), len(sad_test))

    # Select word features
    print("SELECTING WORD FEATURES")
    selected_words = []
    with open(HAPPYSAD_FILEPATH, "r") as infile:
        tokens = [ tokenize(loads(line)[u"text"]) for line in infile ]
        selected_words = selected_word_features(tokens)
    print(len(selected_words))

    # Extract word features from training set
    print("EXTRACTING WORD FEATURES")
    happy_features_set = features_set(happy_tokens, selected_words)
    sad_features_set = features_set(sad_tokens, selected_words)
    print(len(happy_features_set), len(sad_features_set))

    # Train on word features
    print("TRAINING ON WORD FEATURES")
    all_features_sets = happy_features_set + sad_features_set
    samples = listify(all_features_sets)
    labels = [ 1 for _ in happy_features_set ] + [ 0 for _ in sad_features_set ]
    model = GaussianNB()
    model.fit(samples, labels)
    print(len(samples), len(labels))

    # Test on word features
    print("TESTING")
    happy_test_samples = listify(features_set(happy_test, selected_words))
    sad_test_samples = listify(features_set(sad_test, selected_words))
    happy_predictions = model.predict(happy_test_samples)
    sad_predictions = model.predict(sad_test_samples)
    print(sum(happy_predictions), len(sad_predictions)-sum(sad_predictions))

    with open(OUTPUT_FILEPATH, "w") as outfile:
        outfile.write("General stats\n")
        outfile.write("Number of happy samples: {}\n".format(len(all_happy_tokens)))
        outfile.write("Number of sad samples: {}\n".format(len(all_sad_tokens)))
        outfile.write("Happy training: {}\n".format(len(happy_tokens)))
        outfile.write("Sad training: {}\n".format(len(sad_tokens)))
        outfile.write("Happy testing: {}\n".format(len(happy_test)))
        outfile.write("Sad testing: {}\n".format(len(sad_test)))

        outfile.write("\nClassification results\n")
        outfile.write("Number of predicted happy: {} (out of {})\n".format(
            sum(happy_predictions), len(happy_test)))
        outfile.write("Percent correct for happy: {}%\n".format(
            100*sum(happy_predictions) / len(happy_test)))
        outfile.write("Number of predicted sad: {} (out of {})\n".format(
            len(sad_predictions)-sum(sad_predictions), len(sad_test)))
        outfile.write("Percent correct for sad: {}%\n".format(
            100*(len(sad_predictions)-sum(sad_predictions)) / len(sad_test)))
        outfile.write("Total correct: {} (out of {})\n".format(
            sum(happy_predictions) + (len(sad_predictions)-sum(sad_predictions)),
            len(happy_predictions)+len(sad_predictions)
        ))
        outfile.write("Percent correct for all: {}%\n".format(
            100*(sum(happy_predictions)+(len(sad_predictions)-sum(sad_predictions)))/(
                len(happy_predictions)+len(sad_predictions))
        ))

        outfile.write("\nRaw output\n")
        outfile.write("Happy predictions:\n")
        happy_probs = model.predict_proba(happy_test_samples)
        for p in happy_probs:
            outfile.write(str(p))
            outfile.write("\n")
        outfile.write("Sad predictions:\n")
        sad_probs = model.predict_proba(sad_test_samples)
        for p in sad_probs:
            outfile.write(str(p))
            outfile.write("\n")
        outfile.write("Happy test samples:\n")
        for tokens in happy_test:
            outfile.write(str(tokens))
            outfile.write("\n")
        outfile.write("Sad test samples:\n")
        for tokens in sad_test:
            outfile.write(str(tokens))
            outfile.write("\n")
if __name__ == "__main__":
    __main__()
