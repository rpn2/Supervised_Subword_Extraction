#!/usr/bin/env python
# -*- coding: utf-8 -*-



import ast


class prepareData():


    def __init__(self, feature_dict, label_file):

        self.feature_dict = feature_dict
        self.labelfile   = label_file
        self.feat = {}        
        self.labels = {}


    def separate_training(self):

        result_feature = open("data/labelledfeatures.txt", 'w')
        result_label = open("data/labelsdict.txt", 'w')

        with open(self.labelfile, 'r') as source_data:
            for line in source_data:
                wordtemp = line.split(":")
                val = self.feature_dict[wordtemp[0]]
                self.feat[wordtemp[0]] = val
                #result_file.write('{0}:{1}'.format(wordtemp[0],val))
                templst = wordtemp[1].split(",")
                self.labels[wordtemp[0]] = [int(i) for i in templst]

       
        result_feature.write(str(self.feat))
        result_label.write(str(self.labels))

        result_feature.close()
        result_label.close()


    

        

   


if __name__ == '__main__':

    label_file = 'data/labelfile.txt'
    with open('data/dummyfeature.txt', 'r') as fp:
        contents = fp.read()
        featuredict= ast.literal_eval(contents)
        
    pd = prepareData(featuredict,label_file)
    pd.separate_training()
    
    


        




    

        
