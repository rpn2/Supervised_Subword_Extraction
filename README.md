# Semi Supervised Morpheme Extraction

TODO

## Vocabulary Extractor

Given a corpus of text data it generates vocabulary list that will be used by feature extractor. Tokenize provided text 
input data into normalized words. Words are normalized by removing all non-alphanumeric characters and converted to 
lowercase. Uses NLTK stopwords data set to filter stopwords from the resulting data set. Resulting data set contains 
words and their frequency sorted in the descending order of the target word frequency.

We are using [NLTK](https://www.nltk.org/) data to remove the stop words. Before running the program you will need to 
download NLTK stopwords collection.

    > python
    # import NLTK module in your python interpreter
    > import nltk
    # below will open up NLTK downloader window, using the UI download stopwords Corpora
    > nltk.download() 

Once all dependencies are installed you can run the wrapper using the following commands

    # display help message
    > python vocabularyExtractor.py --help
    # running with defaults that assume data/dblp.txt for training data and data/vocabulary.txt for test data
    > python vocabularyExtractor.py
    # explicitly specifying non-default params
    > python vocabularyExtractor.py --input corpusData.txt --output vocabulary.txt

## Feature Extractor

Given a vocabulary list, feature vector for each word is generated. We are using datrie library for generating prefix trees.
You may need to install the lib prior to running the feature extractor.

	# example on how to run vocabulary extractor, creates feature.txt [feature vectors]
    > python vocab2feature.py <input> <output>

## Morpheme Classifier

Given a set of feature vectors, train the classifier model, currently sample predict is available

	# example on how to run classifier
    > python randomforest.py 

TODO


## Baseline

### SentencePiece

We are using SentencePiece, unsupervised text tokenizer for generating baselines. All baseline data results was 
generated using our `sentencePieceDriver.py` script. Script assumes that SentencePiece is already installed on your 
machine and is available from the command line. See [SentencePiece repo](https://github.com/google/sentencepiece) for 
details about the application and how to install it locally. Once installed you can generate the baseline by running

    # display help message
    python sentencePieceDriver.py --help
    # running with defaults that assume data/dblp.txt for training data and data/labels_data.txt for test data
    python sentencePieceDriver.py
    # explicitly specifying non-default params
    python sentencePieceDriver.py --train myTrainData.txt --test myLabeledData.txt --output myResults.txt --prefix abc
    
Script assumes existence of `dblp.txt` and `labels_data.txt` files under `data` directory. Former is used to train the 
algorithm and latter is used to generate `sp_input.txt` which is a clean input data to the application that contains 
single word per line. Script will then train the SentencePiece model for a number of vocabulary sizes for `unigram` 
and `bpe` models as well as evaluate them against the words from labeled data set. Encoded results are then evaluated 
against against `labels_data.txt` dictionary that contains expected split words. Generated word split is considered as 
a success as long as one of the generated split words matches one of the expected data entries. 
