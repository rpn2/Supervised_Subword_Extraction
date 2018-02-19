# Semi Supervised Morpheme Extraction

TODO

## Vocabulary Extractor

Given a corpous of data it generates vocabulary list that will be used by feature extractor.

    # example on how to run vocabulary extractor
    > python vocabularyExtractor.py <input> <output>

## Feature Extractor

Given a vocabulary list, feature vector for each word is generated

	# example on how to run vocabulary extractor, creates Wordsplit.txt (possible split-points, 2-way only) and feature.txt (feature vectors for split points)
    > python vocab2feature.py <input> <output>

## Morpheme Classifier

TODO
