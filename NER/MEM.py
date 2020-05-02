#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pickle

import nltk
from nltk.classify.maxent import MaxentClassifier
from nltk.corpus import gazetteers, names
from sklearn.metrics import (accuracy_score, fbeta_score, precision_score,
                             recall_score)


class MEMM:
    def __init__(self):
        self.train_path = "../data/train"
        self.dev_path = "../data/dev"
        self.beta = 0
        self.max_iter = 0
        self.classifier = None
        self.locations = set(gazetteers.words())
        self.names = set(names.words())
        self.pos = None
        self.previous_labels = None

    # def features_test(self, words, previous_label, next_label, position):
    #     features = {}
    #     current_word = words[position]
    #     previous_word = ''
    #     next_word = ''
    #     if position > 0:
    #         previous_word = words[position-1]
    #     if position < len(words)-1:
    #         next_word = words[position+1]
    #     features['has_(%s)' % current_word] = True
    #     features['prev_label'] = previous_label
    #     # features['next_label'] = next_label
    #     # features['pos'] = self.pos[position]
    #     # if position > 0:
    #     #     features['prev_pos'] = self.pos[position-1]
    # 
    #     if current_word[0].isupper():
    #         features['Capilized'] = True
    #         if current_word.isupper():
    #             features['All caps'] = True
    #         # elif previous_word in {',', '(', ':', '-', '"'}:
    #         #     features['After chosen punctuation'] = True
    #         # elif previous_word.islower():
    #         #     features['Previous word is lower'] = True
    #         if len(current_word) == 2 and current_word[1] == '.':
    #             features['Capitalized char with period'] = True
    #         if len(current_word) >= 2 and current_word[0]+current_word[1:].lower() in self.names:
    #             features['Is a name'] = True
    #         if current_word in self.locations:
    #             features['Is a location'] = True
    #         if next_word in {'says', 'said'}:
    #             features['Next word is says or said'] = True
    #     # elif current_word.islower():
    #     #     features['Lowercase'] = 1
    # 
    #     if position > 0:
    #         previous_word = words[position-1]
    #         if previous_word in {'a', 'an', 'the', 'A', 'An', 'The'}:
    #             features['Not a name'] = True
    #     # if re.search(r'\d+', current_word) is not None:
    #     #     features['Contains digit'] = True
    #     # if current_word in self.previously_recognized:
    #     #     features['Previously recognized'] = 1
    #     # if current_word.find('-') != -1:
    #     #     features['Contains hyphen'] = True
    #     # if current_word.find("'") != -1:
    #     #     features['Contains single quote'] = True
    #     # if current_word.isalpha():
    #     #     features['is alphabetic'] = 1
    #     # if self.pos[position] == 'NNP':
    #     #     features['POS is NNP'] = 1
    # 
    #     return features
    
    def features(self, words, position):
        features = {}
        current_word = words[position]
        previous_word = ''
        next_word = ''
        if position > 0:
            previous_word = words[position-1]
        if position < len(words)-1:
            next_word = words[position+1]
        features['has_(%s)' % current_word] = True
        features['prev_label'] = self.previous_labels[position]
        # features['next_label'] = next_label
        # features['pos'] = self.pos[position]
        # if position > 0:
        #     features['prev_pos'] = self.pos[position-1]

        if current_word[0].isupper():
            features['Capilized'] = True
            if current_word.isupper():
                features['All caps'] = True
            # elif previous_word in {',', '(', ':', '-', '"'}:
            #     features['After chosen punctuation'] = True
            # elif previous_word.islower():
            #     features['Previous word is lower'] = True
            if len(current_word) == 2 and current_word[1] == '.':
                features['Capitalized char with period'] = True
            if len(current_word) >= 2 and (current_word[0] + current_word[1:].lower()) in self.names:
                features['Is a name'] = True
            if current_word in self.locations:
                features['Is a location'] = True
            if next_word in {'says', 'said'}:
                features['Next word is says or said'] = True
        # elif current_word.islower():
        #     features['Lowercase'] = 1

        if position > 0:
            previous_word = words[position-1]
            if previous_word in {'a', 'an', 'the', 'A', 'An', 'The'}:
                features['Not a name'] = True
        # if re.search(r'\d+', current_word) is not None:
        #     features['Contains digit'] = True
        # if current_word in self.previously_recognized:
        #     features['Previously recognized'] = 1
        # if current_word.find('-') != -1:
        #     features['Contains hyphen'] = True
        # if current_word.find("'") != -1:
        #     features['Contains single quote'] = True
        # if current_word.isalpha():
        #     features['is alphabetic'] = 1
        # if self.pos[position] == 'NNP':
        #     features['POS is NNP'] = 1

        return features

    def load_data(self, filename):
        words = []
        labels = []
        for line in open(filename, "r", encoding="utf-8"):
            doublet = line.strip().split("\t")
            if len(doublet) < 2:     # remove emtpy lines
                continue
            words.append(doublet[0])
            labels.append(doublet[1])
        return words, labels

    def train(self):
        print('Training classifier...')

        words, labels = self.load_data(self.train_path)

        self.pos = [t[1] for t in nltk.pos_tag(words)]

        self.previous_labels = ["O"] + labels
        # next_labels = labels[1:] + ['O']

        features = [self.features(words, i)
                    for i in range(len(words))]
        train_samples = [(f, l) for (f, l) in zip(features, labels)]
        classifier = MaxentClassifier.train(
            train_samples, max_iter=self.max_iter)
        self.classifier = classifier

        self.pos = self.previous_labels = None

    def test(self):
        print('Testing classifier...')
        words, labels = self.load_data(self.dev_path)
        self.previous_labels = ["O"] + labels
        # next_labels = labels[1:] + ['O']
        features = [self.features(words, i) for i in range(len(words))]
        results = [self.classifier.classify(n) for n in features]

        f_score = fbeta_score(labels, results, average='macro', beta=self.beta)
        precision = precision_score(labels, results, average='macro')
        recall = recall_score(labels, results, average='macro')
        accuracy = accuracy_score(labels, results)

        print("%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n" %
              ("f_score=", f_score, "accuracy=", accuracy, "recall=", recall,
               "precision=", precision))

        return True

    def test_standford_ner_tagger(self):
        print('Testing classifier...')
        words, labels = self.load_data(self.dev_path)
        from nltk.tag.stanford import StanfordNERTagger
        st = StanfordNERTagger(
            'C:/Users/GGlin/Desktop/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
            'C:/Users/GGlin/Desktop/stanford-ner-2018-10-16/stanford-ner.jar')

        results = [t[1] for t in st.tag(words)]
        for i, t in enumerate(results):
            if t != 'PERSON':
                results[i] = 'O'

        f_score = fbeta_score(labels, results, average='macro', beta=self.beta)
        precision = precision_score(labels, results, average='macro')
        recall = recall_score(labels, results, average='macro')
        accuracy = accuracy_score(labels, results)

        print("%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n" %
              ("f_score=", f_score, "accuracy=", accuracy, "recall=", recall,
               "precision=", precision))

        return True

    def show_samples(self, bound):
        """Show some sample probability distributions.
        """
        words, labels = self.load_data(self.train_path)
        previous_labels = ["O"] + labels
        next_labels = labels[1:] + ['O']
        features = [self.features(words, i)
                    for i in range(len(words))]
        (m, n) = bound
        pdists = self.classifier.prob_classify_many(features[m:n])

        print('  Words          P(PERSON)  P(O)\n' + '-' * 40)
        for (word, label, pdist) in list(zip(words, labels, pdists))[m:n]:
            if label == 'PERSON':
                fmt = '  %-15s *%6.4f   %6.4f'
            else:
                fmt = '  %-15s  %6.4f  *%6.4f'
            print(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))

    def write_results(self, bound):
        words, labels = self.load_data(self.dev_path)
        previous_labels = ["O"] + labels
        next_labels = labels[1:] + ['O']
        features = [self.features(words, i)
                    for i in range(len(words))]
        (m, n) = bound
        pdists = self.classifier.prob_classify_many(features[m:n])

        with open('../dev_results.txt', 'w') as f:
            f.write('  Words          P(PERSON)  P(O)\n' + '-' * 40 + '\n')
            list_errors = []
            for (word, label, pdist) in list(zip(words, labels, pdists))[m:n]:
                if label == 'PERSON':
                    fmt = '  %-15s *%6.4f   %6.4f'
                else:
                    fmt = '  %-15s  %6.4f  *%6.4f'
                f.write(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))
                if (label == 'PERSON' and pdist.prob('PERSON') <= 0.5) or (label == 'O' and pdist.prob('O') < 0.5):
                    f.write('\t X\n')
                    list_errors.append((word, pdist.prob('PERSON'), pdist.prob('O'), label))
                else:
                    f.write('\n')
            f.write('\nError results:\n')
            for word in list_errors:
                if word[3] == 'PERSON':
                    fmt = '  %-15s *%6.4f   %6.4f\n'
                else:
                    fmt = '  %-15s  %6.4f  *%6.4f\n'
                f.write(fmt % (word[0], word[1], word[2]))
        print('Wrote dev_results.txt!')

        words, labels = self.load_data(self.train_path)
        previous_labels = ["O"] + labels
        next_labels = labels[1:] + ['O']
        features = [self.features(words, i)
                    for i in range(len(words))]
        (m, n) = bound
        pdists = self.classifier.prob_classify_many(features[m:n])

        with open('../train_results.txt', 'w') as f:
            f.write('  Words          P(PERSON)  P(O)\n' + '-' * 40 + '\n')
            list_errors = []
            for (word, label, pdist) in list(zip(words, labels, pdists))[m:n]:
                if label == 'PERSON':
                    fmt = '  %-15s *%6.4f   %6.4f'
                else:
                    fmt = '  %-15s  %6.4f  *%6.4f'
                f.write(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))
                if (label == 'PERSON' and pdist.prob('PERSON') <= 0.5) or (label == 'O' and pdist.prob('O') < 0.5):
                    f.write('\t X\n')
                    list_errors.append((word, pdist.prob('PERSON'), pdist.prob('O'), label))
                else:
                    f.write('\n')
            f.write('\nError results:\n')
            for word in list_errors:
                if word[3] == 'PERSON':
                    fmt = '  %-15s *%6.4f   %6.4f\n'
                else:
                    fmt = '  %-15s  %6.4f  *%6.4f\n'
                f.write(fmt % (word[0], word[1], word[2]))
        print('Wrote train_results.txt!')

    def dump_model(self):
        with open('../model.pkl', 'wb') as f:
            pickle.dump(self.classifier, f)

    def load_model(self):
        with open('../model.pkl', 'rb') as f:
            self.classifier = pickle.load(f)

    def predict_sentence(self, text):
        words = nltk.word_tokenize(text)
        self.previous_labels = ['O']
        results = []

        for i, word in enumerate(words):
            feature = self.features(words, i)

            prob = self.classifier.prob_classify(feature).prob('PERSON')
            if prob >= 0.5:
                result = 'PERSON'
            else:
                result = 'O'
            self.previous_labels.append(result)
            results.append(dict(zip(['word', 'result', 'prob'], [word, result, prob])))

        self.previous_labels = None

        return results
