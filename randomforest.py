#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ast
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
#from sklearn.model_selection import KFold
from sklearn import preprocessing
import random
import math
import codecs

class RandomForest:

    def __init__(self, totalfeat, totallabel, labeldata, prob_threshold = 0.3, cv_count = 10, num_trees=50, max_features= "auto", max_depth = None):
        self.tfeat = totalfeat
        self.tlabel = totallabel
        self.num_trees = num_trees  
        self.max_depth = max_depth   
        self.max_features = max_features   
        self.cv_count = cv_count
        self.label_data = labeldata
        self.accuracy = []
        self.tr_accuracy = []
        self.nores = []
        self.wrongres = []
        self.threshold = prob_threshold

    def cross_validation(self):

        for cv in range(self.cv_count):
            self.trainfeat = {}
            self.trainlabels = {}
            self.testfeat = {}
            self.testlabels = {}
            self.predicted = {}
            self.test_train_split()
            self.prepare_tr_vectors()           
            self.model_training()
            self.training_accuracy()
            self.model_predict_prob()
            self.check_accuracy()

        print("Average training accuracy", sum(self.tr_accuracy)/len(self.tr_accuracy))
        print("Average test accuracy", sum(self.accuracy)/len(self.accuracy))
        print("Average nores percentage", sum(self.nores)/len(self.nores))
        print("Average wrongres percentage", sum(self.wrongres)/len(self.wrongres))



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
                pass
            else:
                for val in vallist:
                    totalfeatures.append(val)
                totallabels = totallabels + tmplist

        self.featurevector = pd.DataFrame(totalfeatures)
        self.labels = np.array(totallabels)

    

    # Fit a random forest model
    def model_training(self):

        self.rf = RandomForestClassifier(n_estimators=self.num_trees, max_features = self.max_features, max_depth= self.max_depth)
        self.rf.fit(self.featurevector,self.labels)

    # predict for a given word: Training accuracy
    def training_accuracy(self):

        tr_predicted = {}
        tr_predicted_sw = {}
        
        
        for word, vallist in self.trainfeat.items():
            labellist = []            
            each_word = pd.DataFrame(vallist)
            charprob = self.rf.predict_proba(each_word)
            #Find indices of largest 2 elmements of class probability
            ind = np.argpartition(charprob[:, 1], -2)[-2:]
            prob_list = charprob[:, 1].tolist()
            tr_predicted[word] = [1 if prob_list[x]  >= self.threshold and x in ind.tolist() else 0 for x in range(0, len(prob_list))]
            

        correctres = 0
        
        for word, predlabellist in tr_predicted.items():  
            found = 0
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
                    found = 1
                    break
            sw = word[prev:len(word)]
            subword_list.append(sw)
            if (found == 0 and sw in comparelist):
                correctres = correctres + 1

            tr_predicted_sw[word] = subword_list

        self.tr_accuracy.append(correctres/len(tr_predicted))

        '''fp = codecs.open("data/tr_debug.txt", 'w', 'utf8')
        fp.write(str(tr_predicted_sw))
        fp.close()'''
             

     # predict for a given word: 
    def model_predict_simple(self):

        for word, vallist in self.testfeat.items():            
            each_word = pd.DataFrame(vallist)
            labellist = self.rf.predict(each_word)
            self.predicted[word] = labellist.tolist()

    # Check accuracy
    def check_accuracy(self):

        correctres = 0        
        te_predicted_sw = {}
        nores = 0
        wrongres = 0
        wrongword = {}

        for word, predlabellist in self.predicted.items():  
            indices = [i for i, x in enumerate(predlabellist) if x == 1]
            subword_list = []
            prev = 0
            det_ans = 0
            comparelist = self.label_data[word]            
            for index in indices:
                sw = word[prev:index+1]
                subword_list.append(sw)
                prev = index+1
                if sw in comparelist:
                    correctres = correctres + 1
                    det_ans = 1
                    break
            sw = word[prev:len(word)]
            if sw != word:
                subword_list.append(sw)

            if (det_ans == 0 and sw in comparelist):
                correctres = correctres + 1
                det_ans = 1
            if det_ans == 0:
                if len(subword_list) == 0:
                    nores = nores + 1
                else:
                    wrongres = wrongres + 1
                    lst =[]
                    lst.append(subword_list)
                    lst.append(comparelist)
                    wrongword[word] = lst
            
            lst =[]
            lst.append(subword_list)
            lst.append(comparelist)
            te_predicted_sw[word] = lst

        self.accuracy.append(correctres/len(self.predicted))
        self.nores.append(nores/len(self.predicted))
        self.wrongres.append(wrongres/len(self.predicted))

        fp = codecs.open("data/test_debug.txt", 'w', 'utf8')
        fp.write(str(te_predicted_sw))
        fp.close()

        fp = codecs.open("data/wrong_word.txt", 'w', 'utf8')
        fp.write(str(wrongword))
        fp.close()



    
    # predict for a given word: First prob is for 0(no-split) and second for 1 (split)
    def model_predict_prob(self):

        for word, vallist in self.testfeat.items():                    
            each_word = pd.DataFrame(vallist)
            charprob = self.rf.predict_proba(each_word)
            #Find indices of largest 2 elmements
            ind = np.argpartition(charprob[:, 1], -2)[-2:]
            prob_list = charprob[:, 1].tolist()
            self.predicted[word] = [1 if prob_list[x]  >= self.threshold and x in ind.tolist() else 0 for x in range(0, len(prob_list))]

            

    


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
    threshold = [0.3, 0.4, 0.5]
    for t in threshold:
        print("threshold =", t)
        rfc = RandomForest(featuredict, labeldict, labeldata, prob_threshold = t, cv_count=10, num_trees=100, max_features = 12)
        rfc.cross_validation()

    





