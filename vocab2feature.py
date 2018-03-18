#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import string
import sys

from datrie import BaseTrie


class Vocab2Feature:

    def __init__(self, vocabulary_data, feature_output, num_features=4):

        self.vocabulary_data = vocabulary_data
        self.feature_output = feature_output
        self.num_features = num_features
        self.word_counts = {}  # Key is word, value is a count of word
        self.featuredict = {}  # key is word, value is list of lists (fetaure vector for each character)

        self.trie = BaseTrie(string.ascii_lowercase)
        self.reverse_trie = BaseTrie(string.ascii_lowercase)

    # Parse Input file and store as dictionary
    def parse_input(self):
        total_word_count = 0
        with codecs.open(self.vocabulary_data, 'r', 'utf8') as source_data:
            for line in source_data:
                word, count = line.strip().split(",")
                self.word_counts[word] = int(count)

                self.populate_trie(word=word, prefix_tree=self.trie)
                self.populate_trie(word=word[::-1], prefix_tree=self.reverse_trie)
                total_word_count += 1

        self.generate_template()

    @classmethod
    def populate_trie(cls, word, prefix_tree):
        prefix = u''
        for character in word:
            prefix += character
            prefix_tree.setdefault(prefix, 0)
            prefix_tree[prefix] += 1

    # Generate Feature Vector template
    def generate_template(self):

        for word in self.word_counts.keys():
            chars_word = list(word)
            char_list = []
            for each_char in chars_word:
                char_vector = [None] * self.num_features
                char_list.append(char_vector)
            self.featuredict[word] = char_list

    def write_template(self):
        fp = open(self.feature_output, 'w')
        fp.write(str(self.featuredict))
        fp.close()

    # Populate global character count as dummy fetaure, index is location in feature vector
    def dummy_charcount(self, index):

        char_count = {}
        for word, count in self.word_counts.items():
            chars_word = list(word)
            for each_char in chars_word:
                char_count[each_char] = char_count.get(each_char, 0) + count

        for word, value in self.featuredict.items():
            chars_word = list(word)
            char_list = []
            for charindex in range(len(chars_word)):
                char_vector = value[charindex]
                char_vector[index] = char_count[chars_word[charindex]]
                char_list.append(char_vector)

            self.featuredict[word] = char_list

        fp = open("data/dummyfeature.txt", 'w')
        fp.write(str(self.featuredict))
        fp.close()

    # Helper functions
    def check_worddict(self):

        for key, val in self.word_counts.items():
            print(key, val)

    def check_featuredict(self):

        for key, val in self.featuredict.items():
            print(key, val)


if __name__ == '__main__':

    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = 'data/updated_vocabulary.txt'
        output_file = 'data/feature.txt'

    v2f = Vocab2Feature(input_file, output_file)
    v2f.parse_input()
    v2f.write_template()
    v2f.dummy_charcount(0)
    v2f.dummy_charcount(1)
    v2f.dummy_charcount(2)
    v2f.dummy_charcount(3)



