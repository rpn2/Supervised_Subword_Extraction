#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Executable wrapper for extracting vocabulary from the specified text corpus. Tokenizes text into normalized words
(i.e. converts to lowercase and removes any non alphanumeric characters) and omits stopwords from the result. Utilizes
NLTK stopwords data set for filtering out stopwords.

Example Usage:

    # display help message
    python vocabularyExtractor.py --help
    # running with defaults that assume data/dblp.txt for training data and data/vocabulary.txt for test data
    python vocabularyExtractor.py
    # explicitly specifying non-default params
    python vocabularyExtractor.py --input corpusData.txt --output vocabulary.txt
"""

import argparse
import codecs
import re

from collections import defaultdict
from datetime import datetime
from nltk.corpus import stopwords


def extract_vocabulary(input_file="data/dblp.txt", output_file="data/vocabulary.txt"):
    """Tokenize provided text input data into normalized words. Words are normalized by removing all non-alphanumeric
    characters and converted to lowercase. Uses NLTK stopwords data set to filter stopwords from the resulting data set.
    Resulting data set contains words and their frequency sorted in the descending order of the target word frequency.

    :param input_file: text corpus to be tokenized
    :param output_file: resulting vocabulary file
    """
    print '{0} starting vocabulary extraction [source: {1}, output: {2}]'.format(datetime.now(), input_file, output_file)

    english_stopwords = set(stopwords.words('english'))
    result = defaultdict(int)

    with codecs.open(input_file, 'r', 'utf8') as source_data:
        for title in source_data:
            # split sentences into words
            for word in re.split(r'[ ,.]', title, maxsplit=0):
                # replace anything that is not alphanumeric or hyphen in the resulting words
                normalized_word = re.sub('[^0-9a-z\-]+', '', word.lower()).replace('-', "_")
                if normalized_word and normalized_word not in english_stopwords and '_' != normalized_word:
                    result[normalized_word] += 1

    result_file = codecs.open(output_file, 'w', 'utf8')
    for word in sorted(result, key=result.get, reverse=True):
        # print word, result[word]
        result_file.write('{0},{1}\n'.format(word, result[word]))
    result_file.close()

    print '{0} processed input data and generated {1} vocabulary results'.format(datetime.now(), len(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="vocabularyExtractor tokenizes provided text corpus data into "
                                                 "normalized words omitting stopwords")
    parser.add_argument("--input", default="data/dblp.txt", metavar="<file>",
                        help="Data that will be tokenized. This can be arbitrary text file.")
    parser.add_argument("--output", default="data/vocabulary.txt", metavar="<file>",
                        help="Name of the file where the extracted vocabulary will be stored.")
    args = parser.parse_args()
    extract_vocabulary(args.input, args.output)
