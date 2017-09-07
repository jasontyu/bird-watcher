from __future__ import print_function

HAPPY_FILEPATH = "data/happy_sampled.txt"
SAD_FILEPATH = "data/sad_corpus.txt"
HAPPYSAD_FILEPATH = "data/happysad_equal_corpus.txt"
SOCCER_FILEPATH = "data/soccer_uniq.txt"
OUTPUT_FILEPATH = "data/soccer_output.txt"

def do_everything(TEST_FILEPATH, OUT_FILEPATH):

    from sklearn.naive_bayes import GaussianNB
    from json import loads
    from classify import tokenize
    from crossfold_validation import features_set, listify

    from health_classify import read_and_tokenize, train_classifier
    from crossfold_validation import read_happy_and_sad, select_features

    happy, sad = read_happy_and_sad(HAPPY_FILEPATH, SAD_FILEPATH)
    selected_words = select_features(HAPPYSAD_FILEPATH)
    model = train_classifier(happy, sad, selected_words)

    test = read_and_tokenize(TEST_FILEPATH)
    test_samples = listify(features_set(test, selected_words))



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


    # PLOT
    import matplotlib.pyplot as plt
    from datetime import datetime, timedelta, tzinfo
    from dateutil import parser


    dts = []
    with open(SOCCER_FILEPATH, "r") as infile:
        dts = [ parser.parse(loads(line)["created_at"]) for line in infile ]
    X = [ (dt.replace(tzinfo=None)-datetime.utcfromtimestamp(0).replace(tzinfo=None)).total_seconds() for dt in dts ]
    print(len(X), len(results))



    def running_mean(l, N):
        sum = 0
        result = list( 0 for x in l)

        for i in range( 0, N ):
            sum = sum + l[i]
            result[i] = sum / (i+1)

        for i in range( N, len(l) ):
            sum = sum - l[i-N] + l[i]
            result[i] = sum / N

        return result

    from itertools import izip
    pairs = sorted(izip(X, results), key=lambda t:t[0])
    X, Y = zip(*pairs)
    Y = running_mean([ 100*y for y in Y], len(results))
    # Y1 = [ y[0] for y in probs ]
    # Y2 = [ y[1] for y in probs ]

    plt.plot(X, Y)
    plt.show()
    plt.savefig("data/soccer_over_time.png")

def main():
    do_everything(SOCCER_FILEPATH, OUTPUT_FILEPATH)



if __name__ == "__main__":
    main()
