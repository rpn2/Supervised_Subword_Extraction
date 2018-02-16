#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from collections import defaultdict
from datetime import datetime

if __name__ == '__main__':
    if len(sys.argv) == 3:
        corpus_data = sys.argv[1]
        vocabulary_output = sys.argv[2]
    else:
        corpus_data = 'data/mod.txt'
        vocabulary_output = 'data/vocabulary.txt'

    print '{0} starting vocabulary extraction [SOURCE: {1}, OUTPUT: {2}]'.format(datetime.now(), corpus_data, vocabulary_output)

    result = defaultdict(int)
    with open(corpus_data, 'r') as source_data:
        for title in source_data:
            for word in title.split():
                normalized_word = re.sub(r'\W+', '', word.lower())
                if normalized_word:
                    result[normalized_word] += 1

    result_file = open(vocabulary_output, 'w')
    for word in sorted(result, key=result.get, reverse=True):
        # print word, result[word]
        result_file.write('{0}:{1}\n'.format(word, result[word]))
    result_file.close()

    print '{0} processed input data and generated {1} vocabulary results'.format(datetime.now(), len(result))
