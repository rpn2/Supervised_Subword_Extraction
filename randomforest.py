#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ast
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import prepareData


class RandomForest:

    def __init__(self, totalfeat, totallabel, num_trees = 20):

        self.tfeat = totalfeat
        self.tlabel = totallabel
        self.num_trees = num_trees

    #Split into test and train: TODO
    def test_train(self): 
        

        

    #Combine vectors of all characters in all words to form feature vector set
    def prepare_vectors(self):
        
        totalfeatures = []
        totallabels = []
        
        for word, vallist in self.tfeat.items(): 

            labellist = self.tlabel[word]    
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
    
  
    
    #Fit a random forest model    
    def model_training(self):

        self.rf = RandomForestClassifier(n_estimators=self.num_trees)
        self.rf.fit(self.featurevector,self.labels) 

    #predict for a given word: First prob is for 0(no-split) and second for 1 (split)
    def model_predict(self, word):

        sampletest = self.testfeat[word]        
        charproblist = []
        for sample in sampletest:
            testvector = np.array(sample)
            charprob= (self.rf.predict_proba(testvector.reshape(1, -1))).tolist()            
            charproblist.append(charprob)
            
        print(charproblist)
        
        

if __name__ == '__main__':

    if len(sys.argv) == 3:
        feature_file = sys.argv[1]
        label_file = sys.argv[2]
    else:
        feature_file = 'data/labelledfeatures.txt'
        label_file = 'data/labelsdict.txt'
    
    with open(feature_file, 'r') as fp:
        contents = fp.read()
        featuredict= ast.literal_eval(contents)

    with open(label_file, 'r') as fp1:
        contents = fp1.read()
        labeldict= ast.literal_eval(contents)

    
    rfc = RandomForest(featuredict,labeldict)
    rfc.test_train()
    #rfc.prepare_vectors()
    #rfc.model_training()
    #rfc.model_predict("planning")
    
    
  


