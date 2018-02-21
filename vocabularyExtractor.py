#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from collections import defaultdict
from datetime import datetime
from nltk.corpus import stopwords

if __name__ == '__main__':
    if len(sys.argv) == 3:
        corpus_data = sys.argv[1]
        vocabulary_output = sys.argv[2]
    else:
        corpus_data = 'data/mod.txt'
        vocabulary_output = 'data/new_vocabulary.txt'

    print '{0} starting vocabulary extraction [SOURCE: {1}, OUTPUT: {2}]'.format(datetime.now(), corpus_data, vocabulary_output)

    english_stopwords = set(stopwords.words('english'))
    result = defaultdict(int)
    with open(corpus_data, 'r') as source_data:
        for title in source_data:
            for word in re.split(r' |,|\.', title, maxsplit=0):
                normalized_word = word.strip().lower()
                if normalized_word and normalized_word not in english_stopwords:
                    result[normalized_word] += 1

    result_file = open(vocabulary_output, 'w')
    for word in sorted(result, key=result.get, reverse=True):
        # print word, result[word]
        result_file.write('{0},{1}\n'.format(word, result[word]))
    result_file.close()

    print '{0} processed input data and generated {1} vocabulary results'.format(datetime.now(), len(result))
