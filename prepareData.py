#!/usr/bin/env python
# -*- coding: utf-8 -*-



import ast


class prepareData():


    def __init__(self, feature_dict, label_file):

        self.feature_dict = feature_dict
        self.labelfile   = label_file
        self.trfeat = {}
        self.testfeat = {}
        self.trlabels = {}

    def separate_training(self):

        result_file = open("data/trainingfeature.txt", 'w')
        with open(self.labelfile, 'r') as source_data:
            for line in source_data:
                wordtemp = line.split(":")
                val = self.feature_dict[wordtemp[0]]
                self.trfeat[wordtemp[0]] = val
                result_file.write('{0}:{1}'.format(wordtemp[0],val))
                templst = wordtemp[1].split(",")
                self.trlabels[wordtemp[0]] = [int(i) for i in templst]

        result_file.close()

        for word,val in self.feature_dict.items():
            if word not in self.trfeat:
                self.testfeat[word] = val

    def debuglabels(self):

        for key, val in self.trlabels.items():
            print(key,val)

    def debug(self):

        for key, val in self.trfeat.items():
            print(key,val)  


if __name__ == '__main__':

    label_file = 'data/labelfile.txt'
    with open('data/dummyfeature.txt', 'r') as fp:
        contents = fp.read()
        featuredict= ast.literal_eval(contents)
        
    pd = prepareData(featuredict,label_file)
    pd.separate_training()
    pd.debug()
    


        




    

        
