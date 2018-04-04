#!/usr/bin/env python
# -*- coding: utf-8 -*-



import ast
import codecs

class prepareData():

    def __init__(self, feature_dict, label_dict):

        self.feature_dict = feature_dict        
        self.feat = {}        
        self.labels = label_dict

    def separate_labelled_data(self):

        result_feature = codecs.open("data/labelled_feature.txt", 'w', 'utf8')
        for word,clist in self.feature_dict.items():  
            if word in self.labels:
                self.feat[word] = clist
        result_feature.write(str(self.feat))        
        result_feature.close()
        


if __name__ == '__main__':

    label_file = 'data/labelfile.txt'
    with codecs.open('data/populated_feature.txt', 'r', 'utf8') as fp:
        contents = fp.read()
        featuredict= ast.literal_eval(contents)

    with codecs.open('data/labels_dict.txt', 'r', 'utf8') as lp:
        contents = lp.read()
        labeldict= ast.literal_eval(contents)
        
    pd = prepareData(featuredict,labeldict)
    pd.separate_labelled_data()
    
    


        




    

        
