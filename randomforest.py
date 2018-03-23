#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ast
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import random
import math
import codecs

class RandomForest:

    def __init__(self, totalfeat, totallabel, num_trees=25):
        self.tfeat = totalfeat
        self.tlabel = totallabel
        self.num_trees = num_trees
        self.trainfeat = {}
        self.trainlabels = {}
        self.testfeat = {}
        self.testlabels = {}
        self.predicted = {}

    # Split into test and train: 80% training and 20% test
    def test_train_split(self):
        testkeys = random.sample(self.tfeat.keys(), math.ceil(len(self.tfeat)*0.2))
        for key, val in self.tfeat.items():
            if key in testkeys:
                self.testfeat[key] = val
                self.testlabels[key] = self.tlabel[key]
            else:
                self.trainfeat[key] = val
                self.trainlabels[key] = self.tlabel[key]

    # Combine vectors of all characters in all words to form feature vector set
    def prepare_tr_vectors(self):

        totalfeatures = []
        totallabels = []

        for word, vallist in self.trainfeat.items():

            labellist = self.trainlabels[word]
            tmplist = [labellist[i] for i in range(1,len(labellist),2)]
            if len(tmplist) != len(list(word)):
                #print(word,tmplist)
                pass
            else:
                for val in vallist:
                    totalfeatures.append(val)
                totallabels = totallabels + tmplist

        self.featurevector = np.array(totalfeatures)
        self.labels = np.array(totallabels)

    # Fit a random forest model
    def model_training(self):
        self.rf = RandomForestClassifier(n_estimators=self.num_trees)
        self.rf.fit(self.featurevector,self.labels)

    # predict for a given word: First prob is for 0(no-split) and second for 1 (split)
    def model_predict_simple(self):

        for word, vallist in self.testfeat.items():
            labellist = []
            for each_vector in vallist:
                testvector = np.array(each_vector)
                charprob= self.rf.predict_proba(testvector.reshape(1, -1))
                if charprob[0][1] >= 0.5:
                    labellist.append(1)
                else:
                    labellist.append(0)

            self.predicted[word] = labellist

    # predict for a given word: First prob is for 0(no-split) and second for 1 (split)
    def model_predict_maxlikelihood(self):

        for word, vallist in self.testfeat.items():
            charproblist = []
            for each_vector in vallist:
                testvector = np.array(each_vector)
                charprob= self.rf.predict_proba(testvector.reshape(1, -1))
                charproblist.append(charprob[0][1])
            self.predicted[word] = charproblist


    # Check accuracy
    def check_accuracy_maxlikelihood(self):

        correctres = 0
        for word, predprob  in self.predicted.items():
            tmplist = self.testlabels[word]
            labellist = [tmplist[i] for i in range(1,len(tmplist),2)]
            index_maxprob = max(range(len(predprob)), key=predprob.__getitem__)
            if predprob[index_maxprob] >= 0.5 and labellist[index_maxprob] == 1:
                correctres = correctres + 1

            #Debug
            print(word, labellist, index_maxprob, predprob[index_maxprob])

        # Accuracy calculations to follow
        print(correctres)

    # Check accuracy
    def check_accuracy_simple(self):

        correctres = 0
        for word, predlabellist in self.predicted.items():
            tmplist = self.testlabels[word]
            labellist = [tmplist[i] for i in range(1,len(tmplist),2)]
            if predlabellist == labellist:
                correctres = correctres + 1
            #TODO: Check if lengths of labellists are same
            print(word,labellist,predlabellist)
        # Accuracy calculations to follow
        print(correctres)


if __name__ == '__main__':

    if len(sys.argv) == 3:
        feature_file = sys.argv[1]
        label_file = sys.argv[2]
    else:
        feature_file = 'data/labelledfeatures.txt'
        label_file = 'data/labelsdict.txt'

    with codecs.open(feature_file, 'r', 'utf8') as fp:
        contents = fp.read()
        featuredict = ast.literal_eval(contents)

    with codecs.open(label_file, 'r', 'utf8') as fp1:
        contents = fp1.read()
        labeldict = ast.literal_eval(contents)

    rfc = RandomForest(featuredict, labeldict)
    rfc.test_train_split()
    rfc.prepare_tr_vectors()
    rfc.model_training()
    # rfc.model_predict_maxlikelihood()
    # rfc.check_accuracy_maxlikelihood()
    rfc.model_predict_simple()
    rfc.check_accuracy_simple()





