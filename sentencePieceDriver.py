#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Executable wrapper around sentencepiece, unsupervised text tokenizeer. Assumes sentencepiece is already installed
on your system and can be executed from command line. Please refer to https://github.com/google/sentencepiece for
information on how to install it on your system.

Example Usage:

    # display help message
    python sentencePieceDriver.py --help
    # running with defaults that assume data/dblp.txt for training data and data/labels_data.txt for test data
    python sentencePieceDriver.py
    # explicitly specifying non-default params
    python sentencePieceDriver.py --train myTrainData.txt --test myLabeledData.txt --output myResults.txt --prefix abc
"""

import argparse
import ast
import codecs
import os
import subprocess


def generate_baseline(train_data_file="data/dblp.txt",
                      test_data_file="data/labels_data.txt",
                      result_file="data/sp_results.txt",
                      prefix="dblp"):
    """
    Generates baseline text segmentation results using SentencePiece.

    :param train_data_file: path to the training data set, for better results this should be a large text corpora
    :param test_data_file: labeled data set in dictionary format where keys are words and values are expected
        split/root words/morphemes
    :param result_file: name of the file where to store the results
    :param prefix: prefix that will be used for generated SentencePiece model, vocab and result files
    """

    with codecs.open(test_data_file, 'r', 'utf8') as lp:
        contents = lp.read()
    labeled_data = ast.literal_eval(contents)

    # processed labeled data dict to only save keys. those words will be used to evaluate the generated model
    tmp_test_data = 'tmp_sp_input.txt'
    preprocess_data = open(tmp_test_data, 'w')
    for entry, roots in labeled_data.iteritems():
        preprocess_data.write(entry + '\n')
    preprocess_data.close()

    vocab_sizes = {'unigram': [4000, 8000, 12000, 16000, 19000],
                   'bpe': [4000, 8000, 12000, 16000, 20000, 24000, 28000, 32000]}

    # assumes sentencepiece is already installed and available in the shell
    for model in ['unigram', 'bpe']:
        for vocab_size in vocab_sizes[model]:
            common_prefix = "{prefix}_{type}_{size}".format(**{'prefix': prefix, 'type': model, 'size': vocab_size})
            train_cmd = "spm_train --input={train_data} --model_prefix=data/{common_prefix} " \
                        "--vocab_size={size} --model_type={type}".format(**{'train_data': train_data_file,
                                                                            'common_prefix': common_prefix,
                                                                            'type': model,
                                                                            'size': vocab_size})
            subprocess.call(train_cmd, shell=True)
            encode_cmd = "spm_encode --model=data/{common_prefix}.model < {test_data} > data/{common_prefix}.result"\
                .format(**{'common_prefix': common_prefix, 'test_data': tmp_test_data})
            subprocess.call(encode_cmd, shell=True)

    # generate results, we have a match if any of the split words are present in the corresponding labeled data
    total_count = len(labeled_data)
    results = open(result_file, 'w')
    for model in ['unigram', 'bpe']:
        for vocab_size in vocab_sizes[model]:
            candidates = 0
            matched = 0
            with codecs.open('data/{}_{}_{}.result'.format(prefix, model, vocab_size), 'r', 'utf8') as embedded_data:
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
                model, vocab_size, candidates, matched, total_count, matched * 1.0 / total_count)
            print result
            results.write(result + '\n')
    results.close()
    os.remove(tmp_test_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SentencePieceDriver provides wrapper utility to generate baseline "
                                                 "word splits using sentencepiece")
    parser.add_argument("--train", default="data/dblp.txt", metavar="<file>",
                        help="Data that will be used to train sentencepiece model. This can be arbitrary text file.")
    parser.add_argument("--test", default="data/labels_data.txt", metavar="<file>",
                        help="Labeled data that will be used to test sentencepiece model. Expects file to be in "
                             "dictionary format where keys are test words and values are expected split/root words.")
    parser.add_argument("--output", default="data/sp_results.txt", metavar="<file>",
                        help="Name of the file where the results will be stored.")
    parser.add_argument("--prefix", default="dblp", metavar="prefix", help="Prefix for the generated files.")

    args = parser.parse_args()
    generate_baseline(args.train, args.test, args.output, args.prefix)
