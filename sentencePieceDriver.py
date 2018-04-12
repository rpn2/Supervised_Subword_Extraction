#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import codecs
import subprocess

if __name__ == '__main__':

    with codecs.open('data/labels_data.txt', 'r', 'utf8') as lp:
        contents = lp.read()
    labeled_data = ast.literal_eval(contents)

    preprocess_data = open('data/sp_input.txt', 'w')
    for entry, roots in labeled_data.iteritems():
        preprocess_data.write(entry + '\n')

    vocab_sizes = {'unigram': [4000, 8000, 12000, 16000, 19000],
                   'bpe': [4000, 8000, 12000, 16000, 20000, 24000, 28000, 32000]}

    # assumes sentencepiece is already installed and available in the shell
    for model_type in ['unigram', 'bpe']:
        for vocab_size in vocab_sizes[model_type]:
            train_cmd = "spm_train --input=data/dblp.txt --model_prefix=data/dblp_{type}_{size} --vocab_size={size} --model_type={type}".format(**{'type': model_type, 'size': vocab_size})
            subprocess.call(train_cmd, shell=True)
            encode_cmd = "spm_encode --model=data/dblp_{type}_{size}.model < data/sp_input.txt > data/dblp_{type}_{size}.result".format(**{'type': model_type, 'size': vocab_size})
            subprocess.call(encode_cmd, shell=True)

    total_count = len(labeled_data)
    results = open('data/sp_results.txt', 'w')
    for model_type in ['unigram', 'bpe']:
        for vocab_size in vocab_sizes[model_type]:
            candidates = 0
            matched = 0
            with codecs.open('data/dblp_{}_{}.result'.format(model_type, vocab_size), 'r', 'utf8') as embedded_data:
                for line in embedded_data:
                    normalized_line = line.strip().replace(u'\u2581', '')
                    filtered = normalized_line.split(' ')
                    if len(filtered) > 1:
                        candidates += 1

                    original = normalized_line.replace(' ', '')

                    roots = labeled_data.get(original)
                    for candidate in filtered:
                        if candidate in roots:
                            matched += 1
                            break

            result = 'type={}, vocab_size={} -> found {} morphemes, matched {} out of {} ({})'.format(
                model_type, vocab_size, candidates, matched, total_count, matched * 1.0 / total_count)
            print result
            results.write(result + '\n')
    results.close()

