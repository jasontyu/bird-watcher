from __future__ import print_function
from sklearn.naive_bayes import GaussianNB
from json import loads
from classify import tokenize
from crossfold_validation import features_set, listify


HAPPY_FILEPATH = "data/happy_sampled.txt"
SAD_FILEPATH = "data/sad_corpus.txt"
HAPPYSAD_FILEPATH = "data/happysad_equal_corpus.txt"
HEALTH_FILEPATH = "data/healthcare_uniq.txt"
OUTPUT_FILEPATH = "data/healthcare_output.txt"

def read_and_tokenize(filepath):
    with open(filepath, "r") as infile:
        tokens = [ tokenize(loads(line)[u"text"]) for line in infile ]
    return tokens

def train_classifier(happy, sad, selected_words):

    # Extract word features from training set
    print("EXTRACTING WORD FEATURES")
    happy_features_set = features_set(happy, selected_words)
    sad_features_set = features_set(sad, selected_words)

    # Train on word features
    print("TRAINING ON WORD FEATURES")
    all_features_sets = happy_features_set + sad_features_set
    samples = listify(all_features_sets)
    labels = [ 1 for _ in happy_features_set ] + [ 0 for _ in sad_features_set ]
    model = GaussianNB()
    model.fit(samples, labels)

    return model



def __main__():
    from crossfold_validation import read_happy_and_sad, select_features

    happy, sad = read_happy_and_sad(HAPPY_FILEPATH, SAD_FILEPATH)
    selected_words = select_features(HAPPYSAD_FILEPATH)
    model = train_classifier(happy, sad, selected_words)

    health = read_and_tokenize(HEALTH_FILEPATH)
    test_samples = listify(features_set(health, selected_words))
    results = model.predict(test_samples)

    nhappy = sum(results)
    nsad = len(results)-sum(results)
    ntotal = len(results)

    print("Happy", "Sad", "Total")
    print(nhappy, nsad, ntotal)

    with open(OUTPUT_FILEPATH, "w") as outfile:
        outfile.write("Number of predicted happy: {} (out of {})\n".format(
            nhappy, ntotal))
        outfile.write("Percent predicted happy: {}%\n".format(
            100*nhappy/ ntotal))
        outfile.write("Number of predicted sad: {} (out of {})\n".format(
            nsad, ntotal))
        outfile.write("Percent predicted sad: {}%\n".format(
            100*nsad/ ntotal))

if __name__ == "__main__":
    __main__()
