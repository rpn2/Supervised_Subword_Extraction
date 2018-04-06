#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ast
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import random
import math
import codecs

class RandomForest:

    def __init__(self, totalfeat, totallabel, labeldata,cv_count = 10, num_trees=50):
        self.tfeat = totalfeat
        self.tlabel = totallabel
        self.num_trees = num_trees        
        self.cv_count = cv_count
        self.label_data = labeldata
        self.accuracy = []
        self.tr_accuracy = []


    def cross_validation(self):


        for cv in range(self.cv_count):
            self.trainfeat = {}
            self.trainlabels = {}
            self.testfeat = {}
            self.testlabels = {}
            self.predicted = {}
            self.test_train_split()
            self.prepare_tr_vectors()
            self.label_encoding()
            '''self.model_training()
            self.training_accuracy()
            self.model_predict_simple()
            self.check_accuracy_simple()'''

        print("training accuracy", self.tr_accuracy)
        print("test accuracy", self.accuracy)



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

        self.fc = pd.DataFrame(totalfeatures)
        self.labels = np.array(totallabels)

    def label_encoding(self):

        print(self.fc[1:3])

        self.featurevector =self.fc.iloc[ :,1:11]
        self.le1 = preprocessing.LabelEncoder()
        self.le1.fit(self.fc[12])
        self.featurevector[12] = self.le1.transform(self.fc[12])

        self.le2 = preprocessing.LabelEncoder()
        self.le2.fit(self.fc[13])
        self.featurevector[13] = self.le2.transform(self.fc[13])

        print(self.featurevector[1:3])


    # Fit a random forest model
    def model_training(self):

        self.rf = RandomForestClassifier(n_estimators=self.num_trees)
        self.rf.fit(self.featurevector,self.labels)

    # predict for a given word: Training accuracy
    def training_accuracy(self):

        tr_predicted = {}
        tr_predicted_sw = {}

        for word, vallist in self.trainfeat.items():
            labellist = []
            for each_vector in vallist:
                testvector = np.array(each_vector)
                pval= self.rf.predict(testvector.reshape(1, -1))
                labellist.append(pval)
            tr_predicted[word] = labellist

        correctres = 0
        j = 0;
        for word, predlabellist in tr_predicted.items():  
            indices = [i for i, x in enumerate(predlabellist) if x == 1]
            subword_list = []
            prev = 0
            comparelist = self.label_data[word]            
            for index in indices:
                sw = word[prev:index+1]
                subword_list.append(sw)
                prev = index+1
                if sw in comparelist:
                    correctres = correctres + 1
                    break
            tr_predicted_sw[word] = subword_list

        self.tr_accuracy.append(correctres/len(tr_predicted))

        fp = codecs.open("data/tr_debug.txt", 'w', 'utf8')
        fp.write(str(tr_predicted_sw))
        fp.close()
             
           
        

     # predict for a given word: 
    def model_predict_simple(self):

        for word, vallist in self.testfeat.items():
            labellist = []
            for each_vector in vallist:
                testvector = np.array(each_vector)                
                pval= self.rf.predict(testvector.reshape(1, -1))
                labellist.append(pval)
            self.predicted[word] = labellist

    # Check accuracy
    def check_accuracy_simple(self):

        correctres = 0        
        te_predicted_sw = {}

        for word, predlabellist in self.predicted.items():  
            indices = [i for i, x in enumerate(predlabellist) if x == 1]
            subword_list = []
            prev = 0
            comparelist = self.label_data[word]            
            for index in indices:
                sw = word[prev:index+1]
                subword_list.append(sw)
                prev = index+1
                if sw in comparelist:
                    correctres = correctres + 1
                    break
            te_predicted_sw[word] = subword_list

        self.accuracy.append(correctres/len(self.predicted))

        fp = codecs.open("data/test_debug.txt", 'w', 'utf8')
        fp.write(str(te_predicted_sw))
        fp.close()

    ####Unused functions for now
    # predict for a given word: First prob is for 0(no-split) and second for 1 (split)
    def model_predict_simpleAAAAAA(self):

        for word, vallist in self.testfeat.items():
            labellist = []
            for each_vector in vallist:
                testvector = pd.DataFrame(each_vector)
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


    


if __name__ == '__main__':

    if len(sys.argv) == 3:
        feature_file = sys.argv[1]
        label_file = sys.argv[2]
        label_data = sys.argv[3]
    else:
        feature_file = 'data/labelled_feature.txt'
        label_file = 'data/labels_dict.txt'
        label_data = 'data/labels_data.txt'

    with codecs.open(feature_file, 'r', 'utf8') as fp:
        contents = fp.read()
        featuredict = ast.literal_eval(contents)

    with codecs.open(label_file, 'r', 'utf8') as fp1:
        contents = fp1.read()
        labeldict = ast.literal_eval(contents)

    with codecs.open(label_data, 'r', 'utf8') as fp2:
        contents = fp2.read()
        labeldata = ast.literal_eval(contents)

    #Feature dictionary, label dictionary, cross-validation, number of trees
    rfc = RandomForest(featuredict, labeldict,labeldata,1, 75)
    rfc.cross_validation()

    '''rfc.test_train_split()
    rfc.prepare_tr_vectors()
    rfc.model_training()
    # rfc.model_predict_maxlikelihood()
    # rfc.check_accuracy_maxlikelihood()
    rfc.model_predict_simple()
    rfc.check_accuracy_simple()'''





