#!/usr/bin/env python
# -*- coding: utf-8 -*-



import ast
import codecs

class prepareData():

    def __init__(self, feature_dict, label_file):

        self.feature_dict = feature_dict
        self.labelfile   = label_file
        self.feat = {}        
        self.labels = {}

    def separate_labelled_data(self):

        result_feature = codecs.open("data/labelledfeatures.txt", 'w', 'utf8')
        result_label = codecs.open("data/labelsdict.txt", 'w',  'utf8')

        with open(self.labelfile, 'r') as source_data:
            for line in source_data:
                wordtemp = line.split(":")
                val = self.feature_dict[wordtemp[0]]
                self.feat[wordtemp[0]] = val                
                templst = wordtemp[1].split(",")
                self.labels[wordtemp[0]] = [int(i) for i in templst]
       
        result_feature.write(str(self.feat))
        result_label.write(str(self.labels))
        result_feature.close()
        result_label.close()


if __name__ == '__main__':

    label_file = 'data/labelfile.txt'
    with codecs.open('data/populatedfeature.txt', 'r', 'utf8') as fp:
        contents = fp.read()
        featuredict= ast.literal_eval(contents)
        
    pd = prepareData(featuredict,label_file)
    pd.separate_labelled_data()
    
    


        




    

        
