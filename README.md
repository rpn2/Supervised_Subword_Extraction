# Semi Supervised Morpheme Extraction

TODO

## Vocabulary Extractor

Given a corpous of data it generates vocabulary list that will be used by feature extractor. We are using NLTK data 
to remove the stop words. Before running the program you will need to download NLTK stopwords collection.

    > python
    > import nltk
    # below will open up NLTK downloader window, using the UI download stopwords Corpora
    > nltk.download() 

Once all dependencies are installed you can run the app using the following

    # example on how to run vocabulary extractor
    > python vocabularyExtractor.py <input> <output>

## Feature Extractor

Given a vocabulary list, feature vector for each word is generated

	# example on how to run vocabulary extractor, creates feature.txt [feature vectors]
    > python vocab2feature.py <input> <output>

## Morpheme Classifier

Given a set of feature vectors, train the classifier model, currently sample predict is available

	# example on how to run vocabulary extractor, creates Wordsplit.txt (possible split-points, 2-way only) and feature.txt (feature vectors for split points)
    > python randomforest.py 

TODO
