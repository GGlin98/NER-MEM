import argparse
from MEM import MEM


def main():
    classifier = MEM()

    if arg.train:
        classifier.max_iter = MAX_ITER
        classifier.train(arg.clf)
        classifier.dump_model(arg.clf)
    if arg.dev:
        try:
            classifier.load_model(arg.clf)
            classifier.beta = BETA
            classifier.test(arg.clf)
            # classifier.test_StandfordNERTagger()
        except Exception as e:
            print(e)
    if arg.show:
        try:
            classifier.load_model()
            classifier.show_samples(BOUND)
        except Exception as e:
            print(e)
    if arg.write:
        try:
            classifier.load_model()
            classifier.write_results(BOUND)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', nargs='?', const=True, default=True)
    parser.add_argument('-d', '--dev', nargs='?', const=True, default=True)
    parser.add_argument('-s', '--show', nargs='?', const=True, default=False)
    parser.add_argument('-w', '--write', nargs='?', const=True, default=False)
    parser.add_argument('-c', '--clf', nargs='?', const=True, default="MLP")
    arg = parser.parse_args()

    # ====== Customization ======
    BETA = 0.5
    MAX_ITER = 20
    BOUND = (0, 999999)
    # ==========================

    main()
